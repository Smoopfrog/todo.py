from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Todo(BaseModel):
    id: int
    title: str
    done: bool = False


class TodoCreate(BaseModel):
    title: str


class TodoUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


todo_list: list[Todo] = []
id_counter = 1


def find_todo_by_id(id):
    for todo in todo_list:
        if todo.id == id:
            return todo


@app.get("/todos")
async def list_todos():
    return todo_list


@app.post("/todos")
async def add_todo(body: TodoCreate):
    global id_counter
    new_todo = Todo(id=id_counter, title=body.title)

    id_counter += 1

    todo_list.append(new_todo)
    return new_todo


@app.patch("/todos/{id}")
async def update_todo(id: int, body: TodoUpdate):
    todo = find_todo_by_id(id)

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    if body.title is not None and body.title != "":
        todo.title = body.title

    if body.done is not None:
        todo.done = body.done

    return todo


@app.delete("/todos/{id}")
async def delete_todo(id: int):
    todo = find_todo_by_id(id)

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_list.remove(todo)

    return todo
