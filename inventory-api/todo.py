from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#get all the todo items
todos = {}
@app.get("/get-todo")
def get_items():
    return todos

#create todo items
class Todo(BaseModel):
    title: str
    desc: str

@app.post("/create-tod{todo_id}")
def create_todo(todo_id: int,todo: Todo):
    if todo_id in todos:
        return {"Error":" Item ID already exists"}
    todos[todo_id] = {"title":todo.title,"desc":todo.desc}
    return todos[todo_id]