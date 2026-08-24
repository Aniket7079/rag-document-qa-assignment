from src.chunk import chunk_pages
from src.models import PageDocument


def test_chunking_respects_size():
    page = PageDocument("demo.pdf", 1, "Paragraph one.\n\n" + ("word " * 400))
    chunks = chunk_pages([page], size=300, overlap=50)
    assert len(chunks) > 1
    assert all(len(c.text) <= 300 or len(c.text.split()) <= 1 for c in chunks)


def test_chunk_ids_include_source_and_page():
    page = PageDocument("demo.pdf", 2, "A short page.")
    chunks = chunk_pages([page], size=100, overlap=10)
    assert chunks[0].chunk_id == "demo_p2_c1"
