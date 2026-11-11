from pathlib import Path
import pymupdf
from docx import Document 
def extract_pdf(file_path:str) -> list[dict]:
    extracted_pages=[]
    with pymupdf.open(file_path) as pdf:
        for pagenum,page in enumerate(pdf,start=1):
            text=page.get_text()

            extracted_pages.append({
                "page_number":pagenum,
                "text":text,
            })
    return extracted_pages


def extract_docx(file_path:str)-> list[dict]:
    doc=Document(file_path)

    extracted_content=[]

    for p in doc.paragraphs:
        if p.text.strip():
            extracted_content.append({
                "page_number":None,
                "text":p.text,
            })
    for table in doc.tables:
        for row in table.rows:
            row_text=" | ".join(
                cell.text.strip() for cell in row.cells
            )

            extracted_content.append({
                "page_number":None,
                "text":row_text,
            })
    return extracted_content


def extract_txt(file_path: str) -> list[dict]:
    with open(file_path, "r", encoding="utf-8-sig") as file:
        text = file.read()

    return [{
        "page_number": None,
        "text": text,
    }]


def extract_document(file_path:str)-> list[dict]:
    ext=Path(file_path).suffix.lower()

    if ext==".pdf":
        return extract_pdf(file_path)
    elif ext==".docx":
        return extract_docx(file_path)
    elif ext ==".txt":
        return extract_txt(file_path)

    else:
        raise ValueError(f"Unsupported file type:{ext}")
    


