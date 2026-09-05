"""Shared utilities for en-2-hi evaluation: normalization, file loaders."""

import re
import pathlib
from typing import Dict

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "Data"
OUTPUT_DIR = ROOT_DIR / "outputs"
RESULTS_DIR = ROOT_DIR / "results"
METHODS = ["zero", "few", "cot"]
SAMPLE_IDS = [f"Sample_{i}" for i in range(1, 11)]

# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------

_DEVANAGARI_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")

# Patterns that signal the start of a metadata block
_METADATA_HEADERS = re.compile(
    r"(?:^|\n)\s*(?:"
    r"\*{0,2}\s*केस\s*(?:विवरण|का\s*शीर्षक|विवरण)\s*\*{0,2}\s*:"
    r"|\*{0,2}\s*Case\s*(?:Metadata|Details|Title)\s*\*{0,2}\s*:"
    r"|\*{0,2}\s*संदर्भ\s*\*{0,2}\s*:"
    r"|\*{0,2}\s*References?\s*\*{0,2}\s*:"
    r")",
    re.IGNORECASE,
)

# Lines that look like key:value metadata (case title, bench, counsel, etc.)
_METADATA_INLINE = re.compile(
    r"(?:^|\n)\s*(?:"
    r"\*{0,2}\s*(?:केस|मामला|बेंच|पीठ|वकील|अधिवक्ता|वाक्य|कानूनी\s*सलाहकार)\b.*?:"
    r"|\*{0,2}\s*(?:Bench|Counsel|Case)\b.*?:"
    r")",
    re.IGNORECASE,
)

# HTML / JS ad artifacts found in reference Sample 6
_HTML_ARTIFACTS = [
    re.compile(r"article\s*-\s*inside_post_content_ad_\d+"),
    re.compile(r"\(adsbygoogle\s*=\s*window\.adsbygoogle\s*\|\|\s*\[\]\)\.push\(\{?\}?\);?"),
]


def strip_html_artifacts(text: str) -> str:
    for pat in _HTML_ARTIFACTS:
        text = pat.sub("", text)
    return text


def strip_think_tags(text: str) -> str:
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = re.sub(r"</?think>", "", text)
    return text


def strip_markdown(text: str) -> str:
    # Bold **text**
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    # Italic *text* (only when surrounded by spaces or line boundaries)
    text = re.sub(r"(?<=\s)\*(?!\s)([^*\n]+?)(?<!\s)\*(?=\s|$)", r"\1", text)
    # Bullet markers at line start: "- " or "* " or "*   "
    text = re.sub(r"^[\s]*[-*]\s+", "", text, flags=re.MULTILINE)
    # Markdown headers
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    # Stray backticks
    text = text.replace("`", "")
    return text


def strip_metadata(text: str) -> str:
    """Remove case metadata sections appended to summaries.

    Strategy 1: Find a recognised section header and drop everything from there.
    Strategy 2: If no header found, detect trailing key:value lines and drop them.
    """
    # Strategy 1 — explicit header
    m = _METADATA_HEADERS.search(text)
    if m:
        return text[: m.start()].rstrip()

    # Strategy 2 — trailing inline metadata lines
    lines = text.split("\n")
    cut = len(lines)
    for i in range(len(lines) - 1, -1, -1):
        if _METADATA_INLINE.match(lines[i]):
            cut = i
        elif lines[i].strip() == "":
            # blank line before metadata block — also cut
            if cut < len(lines):
                cut = i
                break
        else:
            # non-metadata, non-blank line → stop scanning
            break
    if cut < len(lines):
        return "\n".join(lines[:cut]).rstrip()
    return text


def normalize_digits(text: str) -> str:
    return text.translate(_DEVANAGARI_DIGITS)


def normalize_whitespace(text: str) -> str:
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)  # trailing spaces
    text = re.sub(r"\n{3,}", "\n\n", text)                   # max 1 blank line
    text = text.strip("\n")                                   # leading/trailing newlines
    text = text + "\n" if text else ""
    return text


def normalize_ellipsis(text: str) -> str:
    return re.sub(r"\.{3,}", "...", text)


def normalize_for_evaluation(text: str) -> str:
    """Full normalization pipeline for evaluation comparison."""
    text = strip_html_artifacts(text)
    text = strip_think_tags(text)
    text = strip_markdown(text)
    text = strip_metadata(text)
    text = normalize_digits(text)
    text = normalize_ellipsis(text)
    text = normalize_whitespace(text)
    return text


# ---------------------------------------------------------------------------
# File loaders
# ---------------------------------------------------------------------------

def load_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def load_references(data_dir: pathlib.Path = DATA_DIR) -> Dict[str, str]:
    """Load all 10 Hindi reference summaries."""
    refs = {}
    for sid in SAMPLE_IDS:
        p = data_dir / sid / "HI_Summary.txt"
        if p.exists():
            refs[sid] = load_text(p)
    return refs


def load_outputs(
    method: str, output_dir: pathlib.Path = OUTPUT_DIR
) -> Dict[str, str]:
    """Load generated summaries for one method (zero/few/cot)."""
    out = {}
    method_dir = output_dir / method
    for sid in SAMPLE_IDS:
        p = method_dir / f"{sid}_HI.txt"
        if p.exists():
            out[sid] = load_text(p)
    return out


def load_all_outputs(output_dir: pathlib.Path = OUTPUT_DIR) -> Dict[str, Dict[str, str]]:
    """Load generated summaries for all three methods."""
    return {m: load_outputs(m, output_dir) for m in METHODS}
