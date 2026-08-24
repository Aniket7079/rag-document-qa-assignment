import re
from .models import Chunk, PageDocument


def _paragraphs(text: str) -> list[str]:
    parts = re.split(r"\n\s*\n", text)
    return [p.strip() for p in parts if p.strip()]


def _split_long(text: str, size: int, overlap: int) -> list[str]:
    words = text.split()
    chunks: list[str] = []
    current: list[str] = []
    length = 0
    for word in words:
        extra = len(word) + (1 if current else 0)
        if current and length + extra > size:
            chunks.append(" ".join(current))
            carry: list[str] = []
            carry_len = 0
            for old_word in reversed(current):
                add = len(old_word) + (1 if carry else 0)
                if carry_len + add > overlap:
                    break
                carry.insert(0, old_word)
                carry_len += add
            current = carry
            length = carry_len
        current.append(word)
        length += extra
    if current:
        chunks.append(" ".join(current))
    return chunks


def chunk_pages(pages: list[PageDocument], size: int = 1200, overlap: int = 150) -> list[Chunk]:
    if size <= overlap:
        raise ValueError("chunk size must be greater than overlap")
    result: list[Chunk] = []
    for page_doc in pages:
        paragraphs = _paragraphs(page_doc.text)
        page_chunks: list[str] = []
        current = ""
        for paragraph in paragraphs:
            candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
            if len(candidate) <= size:
                current = candidate
                continue
            if current:
                page_chunks.append(current)
            if len(paragraph) <= size:
                current = paragraph
            else:
                page_chunks.extend(_split_long(paragraph, size, overlap))
                current = ""
        if current:
            page_chunks.append(current)

        for idx, text in enumerate(page_chunks, start=1):
            chunk_id = f"{page_doc.source.rsplit('.', 1)[0]}_p{page_doc.page}_c{idx}"
            result.append(Chunk(chunk_id, page_doc.source, page_doc.page, idx, text))
    return result
