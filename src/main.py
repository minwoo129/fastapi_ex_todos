from typing import List

from fastapi import FastAPI, Body, HTTPException, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from database.repository import get_todos, get_todo_by_todo_id, create_todo

from database.orm import ToDo
from schema.response import ToDoListSchema, ToDoSchema
from schema.request import CreateToDoRequest

app = FastAPI()

@app.get("/")
def health_check_handler():
    return {"ping": "pong"}

todo_data = {
    1: {
        "id": 1,
        "contents": "실전! FastAPI 섹션 0 수강",
        "is_done": True
    },
    2: {
        "id": 2,
        "contents": "실전! FastAPI 섹션 1 수강",
        "is_done": False
    },
    3: {
        "id": 3,
        "contents": "실전! FastAPI 섹션 2 수강",
        "is_done": False
    }
}

@app.get("/todos", status_code=200)
def get_todos_handler(
        order: str | None = None,
        session: Session = Depends(get_db)
) -> ToDoListSchema:
    todos: List[ToDo] = get_todos(session)
    if order and order == "DESC":
        return ToDoListSchema(
            todos=[ToDoSchema.from_orm(todo) for todo in todos[::-1]]
        )
    return ToDoListSchema(
        todos=[ToDoSchema.from_orm(todo) for todo in todos]
    )

@app.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(
        todo_id: int,
        session: Session = Depends(get_db)
) -> ToDoSchema:
    todo: ToDo | None = get_todo_by_todo_id(session, todo_id)

    if todo:
        return ToDoSchema.from_orm(todo)

    raise HTTPException(status_code=404, detail="Todo Not Found")


@app.post("/todos", status_code=201)
def create_todo_handler(
        request: CreateToDoRequest,
        session: Session = Depends(get_db)
):
    todo: ToDo = ToDo.create(request)
    todo: ToDo = create_todo(session, todo=todo)
    return todo

@app.patch("/todos/{todo_id}", status_code=200)
def update_todo_handler(
        todo_id: int,
        is_done: bool = Body(..., embed=True)
):
    todo = todo_data.get(todo_id)
    if todo:
        todo["is_done"] = is_done
        return todo

    raise HTTPException(status_code=404, detail="Todo Not Found")

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(todo_id: int):
    todo = todo_data.pop(todo_id, None)
    if todo:
        return

    raise HTTPException(status_code=404, detail="Todo Not Found")
