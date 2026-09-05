import os
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
os.environ["HF_HOME"] = str(pathlib.Path(__file__).resolve().parent.parent / ".hf_cache")

import json
import re
import time
from collections import Counter

import pandas as pd
from bert_score import score as bert_score

from utils import (
    METHODS,
    SAMPLE_IDS,
    RESULTS_DIR,
    load_references,
    load_all_outputs,
    normalize_for_evaluation,
)

BERT_MODEL = "google/muril-base-cased"


# ---------------------------------------------------------------------------
# Hindi-compatible ROUGE (the standard rouge-score library only handles ASCII)
# ---------------------------------------------------------------------------

_WORD_RE = re.compile(r"[\u0900-\u097F\u0A00-\u0A7F\u0980-\u09FFA-Za-z0-9]+", re.UNICODE)


def _tokenize(text: str) -> list[str]:
    """Tokenize Hindi/mixed text: split on whitespace, then extract word tokens."""
    tokens = []
    for word in text.lower().split():
        tokens.extend(_WORD_RE.findall(word))
    return [t for t in tokens if len(t) > 0]


def _ngrams(tokens: list[str], n: int) -> list[tuple]:
    return [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def _lcs_length(x: list, y: list) -> int:
    """Longest common subsequence (DP, O(mn))."""
    m, n = len(x), len(y)
    if m == 0 or n == 0:
        return 0
    # space-optimised DP
    prev = [0] * (n + 1)
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr
    return prev[n]


def rouge_score_hindi(ref: str, hyp: str) -> dict:
    """Compute ROUGE-1, ROUGE-2, ROUGE-L for Hindi text."""
    ref_tokens = _tokenize(ref)
    hyp_tokens = _tokenize(hyp)

    result = {}
    for name, n in [("rouge1", 1), ("rouge2", 2)]:
        ref_ngrams = Counter(_ngrams(ref_tokens, n))
        hyp_ngrams = Counter(_ngrams(hyp_tokens, n))
        overlap = sum((ref_ngrams & hyp_ngrams).values())
        ref_total = sum(ref_ngrams.values())
        hyp_total = sum(hyp_ngrams.values())
        precision = overlap / hyp_total if hyp_total else 0.0
        recall = overlap / ref_total if ref_total else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
        result[name] = {"precision": precision, "recall": recall, "fmeasure": f1}

    # ROUGE-L via LCS
    lcs = _lcs_length(ref_tokens, hyp_tokens)
    precision = lcs / len(hyp_tokens) if hyp_tokens else 0.0
    recall = lcs / len(ref_tokens) if ref_tokens else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    result["rougeL"] = {"precision": precision, "recall": recall, "fmeasure": f1}

    return result


def compute_rouge(refs, hyps):
    """Compute Hindi ROUGE scores for a list of reference/hypothesis pairs."""
    results = []
    for ref, hyp in zip(refs, hyps):
        scores = rouge_score_hindi(ref, hyp)
        results.append({
            "rouge1": scores["rouge1"]["fmeasure"],
            "rouge2": scores["rouge2"]["fmeasure"],
            "rougeL": scores["rougeL"]["fmeasure"],
        })
    return results


def compute_bertscore(refs, hyps, lang="hi", model_type=BERT_MODEL, num_layers=12):
    """Compute BERTScore (precision, recall, F1). Process in batches for memory."""
    batch_size = 5
    all_p, all_r, all_f1 = [], [], []

    for i in range(0, len(refs), batch_size):
        batch_refs = refs[i : i + batch_size]
        batch_hyps = hyps[i : i + batch_size]
        P, R, F1 = bert_score(
            batch_hyps,
            batch_refs,
            lang=lang,
            model_type=model_type,
            num_layers=num_layers,
            verbose=False,
            device="cpu",
        )
        all_p.extend(P.tolist())
        all_r.extend(R.tolist())
        all_f1.extend(F1.tolist())

    return [{"bertscore_p": p, "bertscore_r": r, "bertscore_f1": f}
            for p, r, f in zip(all_p, all_r, all_f1)]


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Load data
    print("Loading references and outputs...")
    refs_raw = load_references()
    outputs_raw = load_all_outputs()

    # Normalize all text
    print("Normalizing text...")
    refs = {sid: normalize_for_evaluation(refs_raw[sid]) for sid in SAMPLE_IDS}
    outputs = {
        m: {sid: normalize_for_evaluation(outputs_raw[m][sid]) for sid in SAMPLE_IDS}
        for m in METHODS
    }

    # Prepare aligned lists per method
    aligned = {}
    for m in METHODS:
        aligned[m] = {
            "refs": [refs[sid] for sid in SAMPLE_IDS],
            "hyps": [outputs[m][sid] for sid in SAMPLE_IDS],
        }

    # --- ROUGE ---
    print("Computing ROUGE scores (Hindi-compatible tokenizer)...")
    rouge_results = {}
    for m in METHODS:
        rouge_results[m] = compute_rouge(
            aligned[m]["refs"], aligned[m]["hyps"]
        )
        print(f"  {m}: done")

    # --- BERTScore ---
    print(f"Computing BERTScore with {BERT_MODEL}...")
    print("  (First run downloads the model — this may take a few minutes)")
    bert_results = {}
    for m in METHODS:
        t0 = time.time()
        bert_results[m] = compute_bertscore(
            aligned[m]["refs"], aligned[m]["hyps"]
        )
        dt = time.time() - t0
        print(f"  {m}: done in {dt:.1f}s")

    # --- Merge results into DataFrame ---
    rows = []
    for m in METHODS:
        for i, sid in enumerate(SAMPLE_IDS):
            row = {"sample": sid, "method": m}
            row.update(rouge_results[m][i])
            row.update(bert_results[m][i])
            rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(RESULTS_DIR / "per_case.csv", index=False)
    print(f"\nSaved per-case results -> {RESULTS_DIR / 'per_case.csv'}")

    # --- Summary statistics ---
    summary = {}
    for m in METHODS:
        mdf = df[df["method"] == m]
        summary[m] = {}
        for col in ["rouge1", "rouge2", "rougeL", "bertscore_p", "bertscore_r", "bertscore_f1"]:
            summary[m][col] = {
                "mean": round(mdf[col].mean(), 4),
                "std": round(mdf[col].std(), 4),
                "min": round(mdf[col].min(), 4),
                "max": round(mdf[col].max(), 4),
            }

    with open(RESULTS_DIR / "summary_stats.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"Saved summary stats -> {RESULTS_DIR / 'summary_stats.json'}")

    # --- Overall comparison table (Markdown) ---
    md_lines = [
        "## Overall Comparison",
        "",
        "| Method | ROUGE-1 | ROUGE-2 | ROUGE-L | BERTScore P | BERTScore R | BERTScore F1 |",
        "|:-------|:-------:|:-------:|:-------:|:-----------:|:-----------:|:------------:|",
    ]
    for m in METHODS:
        s = summary[m]
        md_lines.append(
            f"| **{m}** "
            f"| {s['rouge1']['mean']:.4f} +/- {s['rouge1']['std']:.4f} "
            f"| {s['rouge2']['mean']:.4f} +/- {s['rouge2']['std']:.4f} "
            f"| {s['rougeL']['mean']:.4f} +/- {s['rougeL']['std']:.4f} "
            f"| {s['bertscore_p']['mean']:.4f} +/- {s['bertscore_p']['std']:.4f} "
            f"| {s['bertscore_r']['mean']:.4f} +/- {s['bertscore_r']['std']:.4f} "
            f"| {s['bertscore_f1']['mean']:.4f} +/- {s['bertscore_f1']['std']:.4f} |"
        )

    md_lines += [
        "",
        "---",
        "",
        "*BERTScore model: google/muril-base-cased | ROUGE: no stemming (Hindi)*",
        "",
    ]

    (RESULTS_DIR / "overall_comparison.md").write_text(
        "\n".join(md_lines), encoding="utf-8"
    )
    print(f"Saved overall comparison -> {RESULTS_DIR / 'overall_comparison.md'}")

    # --- Print summary to stdout ---
    print("\n" + "=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    for m in METHODS:
        s = summary[m]
        print(f"\n[{m.upper()}]")
        print(f"  ROUGE-1:    {s['rouge1']['mean']:.4f} +/- {s['rouge1']['std']:.4f}")
        print(f"  ROUGE-2:    {s['rouge2']['mean']:.4f} +/- {s['rouge2']['std']:.4f}")
        print(f"  ROUGE-L:    {s['rougeL']['mean']:.4f} +/- {s['rougeL']['std']:.4f}")
        print(f"  BERTScore:  {s['bertscore_f1']['mean']:.4f} +/- {s['bertscore_f1']['std']:.4f} (F1)")

    print(f"\nAll outputs saved to {RESULTS_DIR}/")


if __name__ == "__main__":
    main()
