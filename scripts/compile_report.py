import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))

import pandas as pd

from utils import METHODS, RESULTS_DIR


def md_table(df, columns=None, fmt=".4f"):
    """Render a pandas DataFrame as a Markdown table."""
    if columns:
        df = df[columns]
    lines = []
    # Header
    lines.append("| " + " | ".join(f"**{c}**" for c in df.columns) + " |")
    lines.append("|" + "|".join(":---:" for _ in df.columns) + "|")
    # Rows
    for _, row in df.iterrows():
        cells = []
        for c in df.columns:
            v = row[c]
            if isinstance(v, float):
                cells.append(f"{v:{fmt}}")
            else:
                cells.append(str(v))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main():
    results_dir = RESULTS_DIR
    sections = []

    # --- Header ---
    sections.append("# Evaluation Report -- EN->HI Legal Summarization\n")
    sections.append("Model: Qwen3.5-4B (Q4_K_M) | Dataset: MILDSum (10 samples) | BERTScore: google/muril-base-cased\n")

    # --- Automatic Evaluation ---
    sections.append("## 1. Automatic Evaluation\n")

    # Overall comparison
    overall_path = results_dir / "overall_comparison.md"
    if overall_path.exists():
        sections.append(overall_path.read_text(encoding="utf-8"))
    else:
        sections.append("*Run `python scripts/evaluate.py` first.*\n")

    # Per-case table
    per_case_path = results_dir / "per_case.csv"
    if per_case_path.exists():
        df = pd.read_csv(per_case_path)
        sections.append("### Per-Case Results\n")
        for m in METHODS:
            mdf = df[df["method"] == m][
                ["sample", "rouge1", "rouge2", "rougeL", "bertscore_f1"]
            ]
            mdf = mdf.rename(columns={"bertscore_f1": "BERT_F1"})
            sections.append(f"#### {m.upper()}\n")
            sections.append(md_table(mdf))
            sections.append("")

    # --- Write report ---
    report = "\n".join(sections)
    out_path = results_dir / "final_report.md"
    out_path.write_text(report, encoding="utf-8")
    print(f"Saved final report -> {out_path}")


if __name__ == "__main__":
    main()
