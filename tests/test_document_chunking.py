
from app.services.document_chunking import chunk_document


def test_short_text_returns_one_chunk():
    content = [
        {
            "page_number": 1,
            "text": "This is a short document."
        }
    ]

    chunks = chunk_document(content)

    assert len(chunks) == 1
    assert chunks[0]["text"] == "This is a short document."
    assert chunks[0]["chunk_index"] == 0
    assert chunks[0]["page_number"] == 1


def test_long_text_is_split_into_multiple_chunks():
    content = [
        {
            "page_number": 1,
            "text": "A" * 2500
        }
    ]

    chunks = chunk_document(content)

    assert len(chunks) > 1
    assert all(len(chunk["text"]) <= 1000 for chunk in chunks)


def test_chunks_have_overlap():
    content = [
        {
            "page_number": 1,
            "text": "A" * 2500
        }
    ]

    chunks = chunk_document(content)

    assert chunks[0]["text"][-150:] == chunks[1]["text"][:150]


def test_page_number_is_preserved():
    content = [
        {
            "page_number": 1,
            "text": "First page content."
        },
        {
            "page_number": 2,
            "text": "Second page content."
        }
    ]

    chunks = chunk_document(content)

    assert chunks[0]["page_number"] == 1
    assert chunks[1]["page_number"] == 2


def test_empty_text_is_skipped():
    content = [
        {
            "page_number": 1,
            "text": ""
        },
        {
            "page_number": 2,
            "text": "   "
        }
    ]

    chunks = chunk_document(content)

    assert chunks == []


def test_chunk_indices_are_sequential():
    content = [
        {
            "page_number": 1,
            "text": "First page content."
        },
        {
            "page_number": 2,
            "text": "Second page content."
        }
    ]

    chunks = chunk_document(content)

    assert [chunk["chunk_index"] for chunk in chunks] == [0, 1]


def test_start_index_is_preserved():
    content = [
        {
            "page_number": 1,
            "text": "A" * 2500
        }
    ]

    chunks = chunk_document(content)

    assert chunks[0]["start_index"] == 0
    assert chunks[1]["start_index"] == 850
