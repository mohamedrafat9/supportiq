from pathlib import Path
from uuid import UUID
from fastapi import UploadFile
import hashlib


STORAGE_ROOT = Path(__file__).resolve().parents[2] / "storage" / "documents"

# print(STORAGE_ROOT)

def get_workspace_storage_dir(workspace_id: UUID) -> Path:

    workspace_dir = STORAGE_ROOT / str(workspace_id)
    workspace_dir.mkdir(parents=True, exist_ok=True)

    return workspace_dir

CHUNK_SIZE = 1024 * 1024  #  1MB

# 
async def save_upload_file(
    file: UploadFile,
    workspace_id: UUID,
    document_id: UUID,
) -> tuple[str, str]:
    workspace_dir = get_workspace_storage_dir(workspace_id)

    file_path = workspace_dir / str(document_id)
    temp_path = workspace_dir / f"{document_id}.part"

    hasher=hashlib.sha256()
    temp_file_created=False

    try:
        with temp_path.open("xb") as buffer:
            temp_file_created=True
            while chunk := await file.read(CHUNK_SIZE):
                buffer.write(chunk)
                hasher.update(chunk)

        temp_path.replace(file_path)

    except Exception:
        if temp_file_created:
            temp_path.unlink(missing_ok=True)
        raise

    content_hash = hasher.hexdigest()
    storage_path = str(file_path.relative_to(STORAGE_ROOT))

    return storage_path, content_hash


def finalize_upload_file(
        workspace_id: UUID,
        document_id: UUID,
)-> str:
    workspace_dir = get_workspace_storage_dir(workspace_id)
    temp_path = workspace_dir / f"{document_id}.part"
    file_path = workspace_dir / str(document_id)

    temp_path.replace(file_path)
    return str(file_path.relative_to(STORAGE_ROOT))

def discard_upload_file(
        workspace_id: UUID,
        document_id: UUID,
)-> None:
    workspace_dir = get_workspace_storage_dir(workspace_id)
    temp_path = workspace_dir / f"{document_id}.part"
    temp_path.unlink(missing_ok=True)