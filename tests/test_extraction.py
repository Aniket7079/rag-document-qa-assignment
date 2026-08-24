from pathlib import Path
from src.extract import extract_pdf


def test_product_manual_extracts_tables_and_text():
    docs = Path("data")
    pages = extract_pdf(docs / "Product_Manual.pdf")
    text = "\n".join(p.text for p in pages)
    assert "LED blinking red" in text
    assert "Recovery Bin" in text
    assert "4TB" in text
