from config import get_settings
from pathlib import Path
settings = get_settings()
MIME_TYPES = {
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".txt": "text/plain",
}
def validate_file_metadata(
    filename: str,
    content_type: str|None,
    ) -> str:
    extension = Path(filename).suffix.lower()
    if extension not in settings.ALLOWED_FILE_EXTENSIONS:
        raise ValueError(f"File extension '{extension}' is not allowed. Allowed extensions: {settings.ALLOWED_FILE_EXTENSIONS}")

    expected_mime_type = MIME_TYPES.get(extension)

    actual_mime_type = (
        content_type.split(";")[0].strip().lower()
        if content_type
        else None
    )
    if actual_mime_type != expected_mime_type:
        raise ValueError("File extension and MIME type do not match.")

    return expected_mime_type
