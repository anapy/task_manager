from pydantic import BaseModel


class ListCreate(BaseModel):
    name: str

class ListUpdate(BaseModel):
    name: str

class ListResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True