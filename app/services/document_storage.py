import hashlib
from pathlib import Path
from uuid import UUID
import re

from fastapi import UploadFile

from app.services.document_validation import validate_file_metadata
from config import get_settings


settings = get_settings()


STORAGE_ROOT = Path(__file__).resolve().parents[2] / "storage" / "documents"

def sanitize_filename(filename: str) -> str:
    filename = Path(filename).stem

    filename = re.sub(r"[^\w-]+", "_", filename)
    filename = filename.strip("_.")

    return filename or "unnamed"

def get_workspace_folder_name(
    workspace_name: str,
    workspace_id: UUID,
) -> str:
    safe_name = sanitize_filename(workspace_name)

    return f"{safe_name}__{workspace_id}"

    
def get_workspace_storage_dir(
    workspace_name:str,
    workspace_id: UUID,
) -> Path:
    folder_name=get_workspace_folder_name(
        workspace_name=workspace_name,
        workspace_id=workspace_id,
    )
    workspace_dir = STORAGE_ROOT / folder_name
    workspace_dir.mkdir(parents=True, exist_ok=True)
    return workspace_dir

def get_document_filename(
    original_filename: str,
    document_id: UUID,
) -> str:
    safe_name = sanitize_filename(original_filename)
    extension = Path(original_filename).suffix.lower()

    return f"{safe_name}__{document_id}{extension}"

CHUNK_SIZE = 1024 * 1024  # 1 MB

async def save_upload_file(
    file: UploadFile,
    workspace_name:str,
    workspace_id: UUID,
    document_id: UUID,
) -> tuple[str, str, int]:
    validate_file_metadata(
        filename=file.filename or "",
        content_type=file.content_type,
    )

    workspace_dir = get_workspace_storage_dir(
        workspace_name=workspace_name,
        workspace_id=workspace_id,
    )

    document_filename=get_document_filename(
        original_filename=file.filename or "uploaded_file",
        document_id=document_id,
    )
    temp_path = workspace_dir / f"{document_filename}.part"

    hasher = hashlib.sha256()
    file_size = 0
    temp_file_created = False
    max_file_size = settings.MAX_UPLOAD_FILE_SIZE_MB * 1024 * 1024
    try:
        with temp_path.open("xb") as buffer:
            temp_file_created = True
            while chunk := await file.read(CHUNK_SIZE):
                file_size += len(chunk)
                if file_size > max_file_size:
                    raise ValueError("File exceeds the maximum allowed size.")

                buffer.write(chunk)
                hasher.update(chunk)
    except Exception:
        if temp_file_created:
            temp_path.unlink(missing_ok=True)
        raise

    if file_size <= 0:
        temp_path.unlink(missing_ok=True)
        raise ValueError("Empty files are not allowed.")

    content_hash = hasher.hexdigest()
    temp_storage_path = str(temp_path.relative_to(STORAGE_ROOT))

    return temp_storage_path, content_hash, file_size


def finalize_upload_file(temp_storage_path: str) -> str:
    temp_path = STORAGE_ROOT / temp_storage_path

    final_path = temp_path.with_suffix("")

    temp_path.replace(final_path)

    return str(final_path.relative_to(STORAGE_ROOT))

def discard_upload_file(temp_storage_path: str) -> None:
    temp_path = STORAGE_ROOT / temp_storage_path
    temp_path.unlink(missing_ok=True)


def delete_stored_file(storage_path: str) -> None:
    file_path = STORAGE_ROOT / storage_path
    file_path.unlink(missing_ok=True)