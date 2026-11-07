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

    file = UploadFile(
        filename="test.txt",
        file=BytesIO(b"Hello SupportIQ")
    )

    storage_path, content_hash = await save_upload_file(
        file=file,
        workspace_id=workspace_id,
        document_id=document_id,
    )

    print("Storage path:", storage_path)
    print("Hash:", content_hash)
    print("Hash length:", len(content_hash))

    temp_path = STORAGE_ROOT / storage_path

    print("Temporary file exists:", temp_path.exists())
    print(
        "Final file exists:",
        (temp_path.parent / str(document_id)).exists()
    )

    final_storage_path = finalize_upload_file(
    workspace_id=workspace_id,
    document_id=document_id,
)

    final_path = STORAGE_ROOT / final_storage_path

    print("Final storage path:", final_storage_path)
    print("Temporary file exists after finalize:", temp_path.exists())
    print("Final file exists after finalize:", final_path.exists())

    final_path.unlink(missing_ok=True)

    temp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    asyncio.run(main())