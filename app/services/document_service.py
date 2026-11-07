from sqlalchemy.orm import Session
from app.db.models.documents import Document
from app.db.repositories.document_repository import (
    create_document,
    get_document_by_content_hash,
    get_document_by_id
)
from app.services.document_storage import(
    save_upload_file,
    finalize_upload_file,
    delete_document_file,
    discard_upload_file,
)
from uuid import UUID

def upload_document_service(
    db: Session,
    workspace_id: UUID,
    original_filename: str,
    storage_path: str,
    mime_type: str,
    file_size_bytes: int,
    content_hash: str
) -> Document:
    existing_document = get_document_by_content_hash(
        db=db,
        workspace_id=workspace_id,
        content_hash=content_hash
    )

    if existing_document:
        discard_upload_file(
            workspace_id=workspace_id,
            document_id=existing_document.id
        )
    
    try:
        document = create_document(
            db=db,
            workspace_id=workspace_id,
            original_filename=original_filename,
            storage_path=storage_path,
            mime_type=mime_type,
            file_size_bytes=file_size_bytes,
            content_hash=content_hash
        )

        db.commit()
        db.refresh(document)

        return document
    except Exception:
        db.rollback()
        raise