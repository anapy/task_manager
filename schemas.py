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

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    list_id: int


class TaskUpdate(BaseModel):
    title: str
    description: str | None = None
    completed: bool


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    list_id: int

    class Config:
        from_attributes = True