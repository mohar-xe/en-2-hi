# EN-2-HI: Cross-Lingual Legal Summarization

English-to-Hindi summarization of Indian court judgments using the MILDSum dataset. Compares three prompting strategies (Zero-shot, Few-shot, Chain-of-Thought) with Qwen3.5-4B.

## Setup

```bash
pip install -r requirements.txt
```

## Execution Order

```bash
# 1. Generate summaries (all 3 methods)
python scripts/generate.py --method all

# 2. Evaluate (ROUGE + BERTScore)
python scripts/evaluate.py

# 3. Compile final report
python scripts/compile_report.py
```

## Structure

```
en-2-hi/
├── src/utils.py              # Shared normalization & file loading
├── scripts/
│   ├── generate.py           # Summary generation (Qwen3.5-4B via llama.cpp)
│   ├── evaluate.py           # ROUGE-1/2/L + BERTScore evaluation
│   └── compile_report.py     # Compile final_report.md
├── Data/                     # 10 MILDSum samples (EN judgment + EN/HI summaries)
├── outputs/                  # Generated summaries (zero/few/cot)
└── results/                  # Evaluation CSVs, stats, final report

```

## Generation Options

```bash
# Single method
python scripts/generate.py --method zero
python scripts/generate.py --method few
python scripts/generate.py --method cot

# Custom paths
python scripts/generate.py --method all --data-dir /path/to/Data --output-dir /path/to/outputs

# Local model file (skip download)
python scripts/generate.py --method zero --model-path /path/to/Qwen3.5-4B-Q4_K_M.gguf
```
