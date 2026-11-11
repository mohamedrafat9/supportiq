
import pymupdf

from app.services.document_processing import process_document


def test_process_pdf(tmp_path):
    file_path = tmp_path / "test.pdf"

    with pymupdf.open() as pdf:
        page1 = pdf.new_page()
        page1.insert_text((50, 50), "  First page   content  ")

        page2 = pdf.new_page()
        page2.insert_text((50, 50), "Second page content")

        pdf.save(file_path)

    result = process_document(str(file_path))

    assert len(result) == 2
    assert result[0]["page_number"] == 1
    assert result[0]["text"] == "First page content"
    assert result[1]["page_number"] == 2
    assert result[1]["text"] == "Second page content"


def test_process_txt(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text(
        "  SupportIQ   document processing  ",
        encoding="utf-8"
    )

    result = process_document(str(file_path))

    assert result == [{
        "page_number": None,
        "text": "SupportIQ document processing",
    }]


def test_skip_empty_content(tmp_path):
    file_path = tmp_path / "empty.txt"
    file_path.write_text("   \n   ", encoding="utf-8")

    result = process_document(str(file_path))

    assert result == []
