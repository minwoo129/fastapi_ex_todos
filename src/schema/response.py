from typing import List

from pydantic import BaseModel

class ToDoSchema(BaseModel):
    id: int
    contents: str
    is_done: bool

    class Config:
        orm_mode = True
        from_attributes = True

class ToDoListSchema(BaseModel):
    todos: List[ToDoSchema]
