from pydantic import BaseModel, ConfigDict, Field
class TicketCreate (BaseModel):
    title:str = Field(min_length=1,max_length=255)


class TicketRead(BaseModel):
    model_config=ConfigDict(from_attributes=True) # this will allow pydatic model to read the data from the sqlalchemy instead of hardcoding the casting
    id:int
    title:str
    status:str