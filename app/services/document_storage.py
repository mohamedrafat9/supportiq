from pathlib import Path
from uuid import UUID
from fastapi import UploadFile

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
) -> str:
    workspace_dir = get_workspace_storage_dir(workspace_id)

    file_path = workspace_dir / str(document_id)
    temp_path = workspace_dir / f"{document_id}.part"

    try:
        with temp_path.open("xb") as buffer:
            while chunk := await file.read(CHUNK_SIZE):
                buffer.write(chunk)

        temp_path.replace(file_path)

    except Exception:
        temp_path.unlink(missing_ok=True)
        raise

    return str(file_path.relative_to(STORAGE_ROOT))

