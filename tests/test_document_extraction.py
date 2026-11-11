import pymupdf
import pytest
from docx import Document

from app.services.document_extraction import extract_document


def test_extract_pdf(tmp_path):
    file_path = tmp_path / "test.pdf"

    with pymupdf.open() as pdf:
        page1 = pdf.new_page()
        page1.insert_text((50, 50), "First page content")

        page2 = pdf.new_page()
        page2.insert_text((50, 50), "Second page content")

        pdf.save(file_path)

    result = extract_document(str(file_path))

    assert len(result) == 2
    assert result[0]["page_number"] == 1
    assert "First page content" in result[0]["text"]
    assert result[1]["page_number"] == 2
    assert "Second page content" in result[1]["text"]


def test_extract_docx(tmp_path):
    file_path = tmp_path / "test.docx"

    doc = Document()
    doc.add_paragraph("Company introduction")

    table = doc.add_table(rows=1, cols=2)
    table.cell(0, 0).text = "Product"
    table.cell(0, 1).text = "Price"

    doc.save(file_path)

    result = extract_document(str(file_path))

    assert any("Company introduction" in item["text"] for item in result)
    assert any("Product | Price" in item["text"] for item in result)
    assert all(item["page_number"] is None for item in result)


def test_extract_txt(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("SupportIQ text extraction test", encoding="utf-8")

    result = extract_document(str(file_path))

    assert len(result) == 1
    assert result[0]["page_number"] is None
    assert result[0]["text"] == "SupportIQ text extraction test"


def test_unsupported_file_type(tmp_path):
    file_path = tmp_path / "test.csv"
    file_path.write_text("name,age", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported file type"):
        extract_document(str(file_path))


def test_corrupted_pdf(tmp_path):
    file_path = tmp_path / "corrupted.pdf"
    file_path.write_text("This is not a valid PDF", encoding="utf-8")

    with pytest.raises(Exception):
        extract_document(str(file_path))
