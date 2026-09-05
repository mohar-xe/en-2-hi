import argparse
import sys
import time
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))

from utils import SAMPLE_IDS, strip_think_tags

# ---------------------------------------------------------------------------
# Model config
# ---------------------------------------------------------------------------

REPO_ID = "unsloth/Qwen3.5-4B-GGUF"
GGUF_FILE = "Qwen3.5-4B-Q4_K_M.gguf"

SYSTEM_PROMPT = (
    "You are an expert legal summarizer. Respond only in Hindi (Devanagari). "
    "English words can be used if no equivalent Hindi word exists."
)

# ---------------------------------------------------------------------------
# Prompts (extracted from generation_notebook.ipynb)
# ---------------------------------------------------------------------------

PROMPTS = {
    "zero": lambda full_text: f"""You are an expert legal journalist. Convert the following court judgment into a concise, readable news summary. The summary must capture the essence of the judgment — who, what, when, where, why, and the final ruling — in a continuous flowing narrative.

    Follow these rules strictly:

    1. Lead with the key ruling: Start with the court name, date, and the core direction or decision in one powerful opening sentence.
    2. Maintain chronological flow: Present facts, arguments, and the final order in the sequence they appear in the judgment.
    3. Include critical quotes: Incorporate 2-3 essential quotes from the judgment verbatim, enclosed in double quotation marks.
    4. Preserve all parties and amounts: Mention the petitioner, respondent(s), and any specific monetary amounts or orders exactly as stated.
    5. End with case metadata: Conclude with the case title, bench name, and counsel names exactly as they appear.
    6. No editorializing: Do not add opinions, interpretations, or commentary. Stick strictly to what the judgment states.
    7. Continuous text: Write as a cohesive news article — no bullet points, no markdown formatting, no section headers. Just flowing paragraphs.

    Judgment Text: {full_text}

    Summary:""",

    "few": lambda full_text: f"""You are an expert legal journalist. Convert the following court judgments into concise, readable news summaries in HINDI. The summary must capture the essence of the judgment — who, what, when, where, why, and the final ruling — in a continuous flowing narrative.

    Follow these rules strictly:
    1. Lead with the key ruling: Start with the court name, date, and the core direction or decision in one powerful opening sentence (in Hindi).
    2. Maintain chronological flow: Present facts, arguments, and the final order in the sequence they appear in the judgment.
    3. Include critical quotes: Incorporate 2-3 essential quotes from the judgment verbatim, enclosed in double quotation marks.
    4. Preserve all parties and amounts: Mention the petitioner, respondent(s), and any specific monetary amounts or orders exactly as stated.
    5. End with case metadata: Conclude with the case title, bench name, and counsel names exactly as they appear.
    6. No editorializing: Do not add opinions, interpretations, or commentary. Stick strictly to what the judgment states.
    7. Continuous text: Write as a cohesive news article — no bullet points, no markdown formatting, no section headers. Just flowing paragraphs.

    ### Example 1
    Judgment Text: 1. The petitioner, Ramesh Singh, has filed the present writ petition challenging the termination order dated 12.05.2021 passed by the Municipal Corporation of Delhi (Respondent No. 2). 2. The petitioner was appointed as a Junior Clerk in 2010. He was terminated on grounds of unauthorized absence from duty. 3. Learned counsel for the petitioner argued that the petitioner was suffering from tuberculosis and had submitted medical certificates. 4. The Court observed that procedural fairness must be maintained. "Termination of services without holding a regular inquiry violates the mandate of Article 311(2) of the Constitution." 5. Consequently, the termination is quashed and the petitioner is reinstated with 50% back wages. Case Title: Ramesh Singh v. MCD. Bench: Justice A. Kumar. Counsel: Mr. X for Petitioner, Mr. Y for Respondent.
    Summary: दिल्ली हाई कोर्ट ने 12 अक्टूबर 2023 को एक याचिका को स्वीकार करते हुए नगर निगम दिल्ली द्वारा रमेश सिंह की सेवाएं समाप्त करने के आदेश को निरस्त कर दिया और उन्हें 50 प्रतिशत पिछली वेतन के साथ बहाल करने का निर्देश दिया। याचिकाकर्ता, जिन्हें 2010 में जूनियर क्लर्क के रूप में नियुक्त किया गया था, पर अनधिकृत अनुपस्थिति का आरोप लगाया गया था। याचिकाकर्ता के वकील ने दलील दी कि याचिकाकर्ता क्षय रोग से पीड़ित थे और उन्होंने चिकित्सा प्रमाण पत्र भी प्रस्तुत किए थे। न्यायालय ने प्रक्रियात्मक न्याय के सिद्धांत को स्थापित करते हुए टिप्पणी की कि "सेवाओं की समाप्ति नियमित जांच किए बिना संविधान के अनुच्छेद 311(2) के आदेश का उल्लंघन करती है।" इस प्रकार, याचिका को स्वीकार कर लिया गया। मामला: रमेश सिंह बनाम एमसीडी। पीठ: जस्टिस ए कुमार। अधिवक्ता: याचिकाकर्ता के लिए श्री एक्स, प्रतिवादी के लिए श्री वाई।

    ### Example 2
    Judgment Text: 1. The appellant, Sita Ram, has filed an appeal against the High Court's judgment dismissing his suit for specific performance of a sale agreement dated 05.01.2010 concerning a 500 sq. yards plot valued at Rs. 50 lakhs. 2. The respondent, Mohan Lal, refused to execute the sale deed citing delay in payment. 3. The Supreme Court allowed the appeal, holding that the delay was minimal. "Time is the essence of contract in specific performance and the delay of 15 days is not sufficient to repudiate the agreement." 4. The respondent is directed to execute the sale deed upon payment of balance Rs. 30 lakhs within four weeks. Case Title: Sita Ram v. Mohan Lal. Bench: Justices B. Rao and C. Singh. Counsel: Mr. A for Appellant, Mr. B for Respondent.
    Summary: भारत के सर्वोच्च न्यायालय ने 22 सितंबर 2022 को एक अपील को स्वीकार करते हुए उच्च न्यायालय के फैसले को पलट दिया और 50 लाख रुपये के 500 वर्ग गज की भूखंड के विक्रय समझौते के विशिष्ट कार्यान्वयन के लिए प्रतिवादी मोहन लाल को विक्रय पत्र पंजीकृत करने का निर्देश दिया। वादी सीता राम ने दलील दी कि प्रतिवादी ने भुगतान में देरी का हवाला देते हुए दस्तावेज़ निष्पादित करने से इनकार कर दिया। सर्वोच्च न्यायालय ने पाया कि भुगतान में 15 दिन की देरी अनुबंध को समाप्त करने के लिए पर्याप्त नहीं है और स्पष्ट रूप से कहा कि "विशिष्ट कार्यान्वयन में समय अनुबंध का सार है और 15 दिन की देरी समझौते को खारिज करने के लिए पर्याप्त नहीं है।" प्रतिवादी को शेष 30 लाख रुपये के भुगतान पर चार सप्ताह के भीतर विक्रय पत्र निष्पादित करने का निर्देश दिया गया। मामला: सीता राम बनाम मोहन लाल। पीठ: जस्टिस बी राव और जस्टिस सी सिंह। अधिवक्ता: अपीलकर्ता के लिए श्री ए, प्रतिवादी के लिए श्री बी।

    ### Target Judgment
    Judgment Text: {full_text}
    Summary:""",

    "cot": lambda full_text: f"""You are an expert legal journalist. Convert the following court judgment into a concise, readable news summary in HINDI. The summary must capture the essence of the judgment — who, what, when, where, why, and the final ruling — in a continuous flowing narrative.

    Follow these rules strictly for the final summary:
    1. Lead with the key ruling: Start with the court name, date, and the core direction or decision in one powerful opening sentence (in Hindi).
    2. Maintain chronological flow: Present facts, arguments, and the final order in the sequence they appear in the judgment.
    3. Include critical quotes: Incorporate 2-3 essential quotes from the judgment verbatim, enclosed in double quotation marks.
    4. Preserve all parties and amounts: Mention the petitioner, respondent(s), and any specific monetary amounts or orders exactly as stated.
    5. End with case metadata: Conclude with the case title, bench name, and counsel names exactly as they appear.
    6. No editorializing: Do not add opinions, interpretations, or commentary. Stick strictly to what the judgment states.
    7. Continuous text: Write as a cohesive news article — no bullet points, no markdown formatting, no section headers. Just flowing paragraphs.

    Before writing the final summary, you must think step-by-step. In your thinking process:

    1. Main facts
    2. Legal issue
    3. Court's reasoning
    4. Final decision/order
    5. Important parties, dates, amounts, and 2-3 essential verbatim quotes
    6. Court name, case title, bench, and counsel names

    The output should contain ONLY the final Hindi summary written strictly according to the 7 rules above (continuous text, no markdown, no bullets).

    Judgment Text: {full_text}

    Summary:""",
}

# Max tokens per method (Model sometimes goes on thinking tangent -> unpredictable so 20k set.)
MAX_TOKENS = {"zero": 20000, "few": 20000, "cot": 20000}


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------

def load_model(model_path=None):
    """Download (if needed) and load the GGUF model on CPU."""
    try:
        from llama_cpp import Llama
    except ImportError:
        print("ERROR: llama-cpp-python not installed. Run: pip install llama-cpp-python")
        sys.exit(1)

    if model_path:
        gguf_path = model_path
    else:
        try:
            from huggingface_hub import hf_hub_download
        except ImportError:
            print("ERROR: huggingface_hub not installed. Run: pip install huggingface_hub")
            sys.exit(1)
        print(f"Downloading {REPO_ID}/{GGUF_FILE}...")
        gguf_path = hf_hub_download(REPO_ID, filename=GGUF_FILE)
        print(f"Downloaded: {pathlib.Path(gguf_path).stat().st_size / 1e9:.2f} GB")

    print("Loading model on CPU (this may take a minute)...")
    llm = Llama(
        model_path=gguf_path,
        n_ctx=49152,
        n_gpu_layers=0,  # CPU only
        n_threads=4,
        verbose=False,
        chat_format="qwen",
    )
    print("[OK] Model loaded")
    return llm


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

def generate(llm, prompt, system=None, max_tokens=32000, temp=0.0):
    """Generate text using llama.cpp chat completion."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    out = llm.create_chat_completion(
        messages=messages,
        max_tokens=max_tokens,
        temperature=temp,
        top_p=0.9,
        repeat_penalty=1.1,
    )
    content = out["choices"][0]["message"]["content"].strip()
    content = strip_think_tags(content)
    return content


def summarize_judgment(llm, method, full_text):
    """Generate a Hindi summary using the specified prompting method."""
    prompt_fn = PROMPTS[method]
    max_tok = MAX_TOKENS[method]
    return generate(llm, prompt_fn(full_text), system=SYSTEM_PROMPT, max_tokens=max_tok, temp=0.0)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate Hindi summaries from English legal judgments")
    parser.add_argument(
        "--method", choices=["zero", "few", "cot", "all"], default="all",
        help="Prompting method to use (default: all)"
    )
    parser.add_argument(
        "--data-dir", type=pathlib.Path, default=None,
        help="Path to Data/ directory (default: auto-detect)"
    )
    parser.add_argument(
        "--output-dir", type=pathlib.Path, default=None,
        help="Path to outputs/ directory (default: auto-detect)"
    )
    parser.add_argument(
        "--model-path", type=pathlib.Path, default=None,
        help="Path to local GGUF file (default: download from HuggingFace)"
    )
    args = parser.parse_args()

    # Resolve paths relative to project root
    project_root = pathlib.Path(__file__).resolve().parent.parent
    data_dir = args.data_dir or (project_root / "Data")
    output_dir = args.output_dir or (project_root / "outputs")

    methods = ["zero", "few", "cot"] if args.method == "all" else [args.method]

    # Validate data exists
    if not data_dir.exists():
        print(f"ERROR: Data directory not found: {data_dir}")
        sys.exit(1)
    sample_dirs = sorted(data_dir.glob("Sample_*"))
    if not sample_dirs:
        print(f"ERROR: No Sample_* directories found in {data_dir}")
        sys.exit(1)
    print(f"Found {len(sample_dirs)} samples in {data_dir}")

    # Load model once
    llm = load_model(model_path=args.model_path)

    # Generate for each method
    for method in methods:
        print(f"\n{'='*60}")
        print(f"  METHOD: {method.upper()}")
        print(f"{'='*60}")

        method_dir = output_dir / method
        method_dir.mkdir(parents=True, exist_ok=True)

        for sdir in sample_dirs:
            sid = sdir.name
            out_path = method_dir / f"{sid}_HI.txt"

            # Skip if already processed
            if out_path.exists() and out_path.stat().st_size > 100:
                print(f"[Skip] {sid}")
                continue

            judgment_path = sdir / "EN_Judgment.txt"
            if not judgment_path.exists():
                print(f"[Error] Missing judgment file: {judgment_path}")
                continue

            judgment = judgment_path.read_text(encoding="utf-8")
            print(f"[{sid}] {len(judgment.split())} words", flush=True)

            t0 = time.time()
            try:
                hi = summarize_judgment(llm, method, judgment)
                hi = hi.strip()
            except Exception as e:
                hi = f"[ERROR: {type(e).__name__}: {e}]"
                print(f"  Error: {e}", flush=True)

            dt = time.time() - t0

            # Log results
            has_hi = any('\u0900' <= c <= '\u097F' for c in hi)
            preview = hi[:200].replace("\n", " ")
            print(f"  Done in {dt:.1f}s | Hindi: {has_hi}", flush=True)
            print(f"  Preview: {preview}...", flush=True)

            out_path.write_text(hi, encoding="utf-8")
            print(f"[Saved] {out_path}\n", flush=True)

    print("Generation complete.")


if __name__ == "__main__":
    main()
