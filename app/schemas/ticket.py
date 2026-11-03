from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


TicketStatus = Literal[
    "open",
    "in_progress",
    "resolved",
    "closed",
]


class TicketCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)


class TicketRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    status: TicketStatus


class TicketUpdate(BaseModel):
    status: TicketStatus