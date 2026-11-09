from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, File, UploadFile, status, HTTPException
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.schemas.document import DocumentRead
from app.services.document_service import upload_document_service
from app.services.document_storage import save_upload_file
from app.db.repositories.workspace_repository import get_workspace_by_id
router = APIRouter(
    tags=["Documents"],
)


@router.post(
    "/workspaces/{workspace_id}/documents",
    response_model=DocumentRead,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    workspace_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    ):
    document_id = uuid4()

    workspace = get_workspace_by_id(
        db=db,
        workspace_id=workspace_id,
    )
    if workspace is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found.",
        )

    temp_storage_path, content_hash, file_size = await save_upload_file(
        file=file,
        workspace_name=workspace.name,
        workspace_id=workspace_id,
        document_id=document_id,
    )

    document = upload_document_service(
        db=db,
        workspace_id=workspace_id,
        document_id=document_id,
        temp_storage_path=temp_storage_path,
        original_filename=file.filename or "uploaded_file",
        mime_type=file.content_type or "application/octet-stream",
        file_size_bytes=file_size,
        content_hash=content_hash,
    )

    return document