from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
DocumentStatus = Literal[
    "uploaded",
    "processing",
    "completed",
    "failed",
]

class DocumentRead(BaseModel):
    id:UUID = Field(..., description="The unique identifier of the document")
    workspace_id:UUID = Field(..., description="The unique identifier of the workspace")
    original_filename:str = Field(..., description="The original filename of the document")
    mime_type:str
    file_size_bytes: int
    status:DocumentStatus
    created_at:datetime

    model_config = ConfigDict(from_attributes=True)