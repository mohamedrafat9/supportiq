from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.documents import Document

def get_document_by_content_hash(
        db:Session,
        workspace_id:UUID,
        content_hash:str
    ) -> Document | None:
    satatement = select(Document).where(
        Document.workspace_id == workspace_id,
        Document.content_hash == content_hash
    )

    return db.scalar(satatement)

def create_document(
        db:Session,
        document_id:UUID,
        workspace_id:UUID,
        original_filename:str,
        storage_path:str,
        mime_type:str,
        file_size_bytes:int,
        content_hash:str
    ) -> Document:
    document = Document(
        id=document_id,
        workspace_id=workspace_id,
        original_filename=original_filename,
        storage_path=storage_path,
        mime_type=mime_type,
        file_size_bytes=file_size_bytes,
        content_hash=content_hash
    )

    db.add(document)
    db.flush()
    return document

def get_document_by_id(
        db:Session,
        document_id:UUID
    ) -> Document | None:

    return db.get(Document, document_id)