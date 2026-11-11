from app.services.document_extraction import extract_document
from app.services.text_cleaning import clean_text

def process_document(file_path:str)-> list[dict]:
    extracted_content=extract_document(file_path)

    processed_content=[]

    for item in extracted_content:
        cleaned_text=clean_text(item["text"])

        if not cleaned_text:
            continue

        processed_content.append({
            "page_number":item["page_number"],
            "text":cleaned_text
        })
    return processed_content