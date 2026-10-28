from pydantic import BaseModel, ConfigDict, Field
from typing import Literal

class TicketCreate (BaseModel): 
    title:str = Field(min_length=1,max_length=255)


class TicketRead(BaseModel):
    model_config=ConfigDict(from_attributes=True) # this will allow pydatic model to read the data from the sqlalchemy instead of hardcoding the casting
    id:int
    title:str
    status: Literal[
        "open",
        "in_progress",
        "resolved",
        "closed",
    ]


class TicketUpdate(BaseModel):
    status: Literal[
        "open",
        "in_progress",
        "resolved",
        "closed",
    ]
