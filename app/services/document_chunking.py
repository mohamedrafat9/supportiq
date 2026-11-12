from langchain_text_splitters import RecursiveCharacterTextSplitter


splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
    length_function=len,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        "",
    ],
    add_start_index=True,
    strip_whitespace=True,
)


def chunk_document(processed_content: list[dict]) -> list[dict]:
    chunks = []

    for item in processed_content:
        text = item["text"]

        if not text.strip():
            continue

        documents = splitter.create_documents([text])

        for document in documents:
            chunks.append({
                "chunk_index": len(chunks),
                "page_number": item["page_number"],
                "start_index": document.metadata["start_index"],
                "text": document.page_content,
            })

    return chunks
