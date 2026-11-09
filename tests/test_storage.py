
import asyncio
from io import BytesIO
from uuid import uuid4

from fastapi import UploadFile

from app.services.document_storage import (
    save_upload_file,
    STORAGE_ROOT,
    finalize_upload_file,
)


async def main():
    workspace_id = uuid4()
    document_id = uuid4()
    workspace_name = "Test Workspace"

    file = UploadFile(
        filename="test.txt",
        file=BytesIO(b"Hello SupportIQ"),
        headers={"content-type": "text/plain"},
    )

    temp_storage_path = None
    final_storage_path = None

    try:
        temp_storage_path, content_hash, file_size = await save_upload_file(
            file=file,
            workspace_name=workspace_name,
            workspace_id=workspace_id,
            document_id=document_id,
        )

        print("Temporary storage path:", temp_storage_path)
        print("Hash:", content_hash)
        print("Hash length:", len(content_hash))
        print("File size:", file_size)

        temp_path = STORAGE_ROOT / temp_storage_path

        print("Temporary file exists:", temp_path.exists())

        final_storage_path = finalize_upload_file(temp_storage_path)

        final_path = STORAGE_ROOT / final_storage_path

        print("Final storage path:", final_storage_path)
        print("Temporary file exists after finalize:", temp_path.exists())
        print("Final file exists after finalize:", final_path.exists())

    finally:
        if final_storage_path:
            (STORAGE_ROOT / final_storage_path).unlink(missing_ok=True)

        if temp_storage_path:
            (STORAGE_ROOT / temp_storage_path).unlink(missing_ok=True)


if __name__ == "__main__":
    asyncio.run(main())
