import re
from pathlib import Path
import fitz

from .models import PageDocument


def _clean_text(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf(path: Path) -> list[PageDocument]:
    pages: list[PageDocument] = []
    with fitz.open(path) as pdf:
        for page_no, page in enumerate(pdf, start=1):
            blocks = page.get_text("blocks")
            blocks = [b for b in blocks if len(b) >= 5 and b[4].strip()]
            blocks.sort(key=lambda b: (round(b[1], 1), round(b[0], 1)))
            text = "\n".join(b[4].strip() for b in blocks)
            text = _clean_text(text)
            if text:
                pages.append(PageDocument(source=path.name, page=page_no, text=text))
    return pages


def extract_corpus(data_dir: Path) -> list[PageDocument]:
    pages: list[PageDocument] = []
    for path in sorted(data_dir.glob("*.pdf")):
        pages.extend(extract_pdf(path))
    if not pages:
        raise FileNotFoundError(f"No PDF files found in {data_dir}")
    return pages
