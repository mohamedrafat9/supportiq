from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.models.documents import Document
from app.db.repositories.document_repository import (
    create_document,
    get_document_by_content_hash,
)
from app.services.document_storage import (
    finalize_upload_file,
    delete_stored_file,
    discard_upload_file,
)

def upload_document_service(
    db: Session,
    workspace_id: UUID,
    document_id:UUID,
    temp_storage_path: str,
    original_filename: str,
    mime_type: str,
    file_size_bytes: int,
    content_hash: str,
) -> Document:

    final_storage_path = None
    committed = False

    try:
        existing_document = get_document_by_content_hash(
            db=db,
            workspace_id=workspace_id,
            content_hash=content_hash,
        )

        if existing_document:
            discard_upload_file(
                temp_storage_path
            )
            return existing_document

        
        final_storage_path = finalize_upload_file(
            temp_storage_path
        )

        document = create_document(
            db=db,
            document_id=document_id,
            workspace_id=workspace_id,
            original_filename=original_filename,
            storage_path=final_storage_path,
            mime_type=mime_type,
            file_size_bytes=file_size_bytes,
            content_hash=content_hash,
        )

        db.commit()
        committed = True

        db.refresh(document)

        return document

    except IntegrityError:
        db.rollback()

        existing_document = get_document_by_content_hash(
            db=db,
            workspace_id=workspace_id,
            content_hash=content_hash,
        )

        if final_storage_path is not None:
            delete_stored_file(final_storage_path)
        else:
            discard_upload_file(temp_storage_path)

        if existing_document:
            return existing_document

        raise

    except Exception:
        db.rollback()

        if final_storage_path is not None and not committed:
            delete_stored_file(final_storage_path)
        elif final_storage_path is None:
            discard_upload_file(temp_storage_path)

        raise
