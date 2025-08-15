from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# In-memory database (list)
todo_list = []

# Data model
class ToDo(BaseModel):
    id: int
    task: str
    completed: bool = False

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI To-Do App"}

@app.get("/todos")
def get_todos():
    return todo_list

@app.post("/todos")
def add_todo(todo: ToDo):
    todo_list.append(todo)
    return {"message": "To-Do added successfully"}

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated: ToDo):
    for index, todo in enumerate(todo_list):
        if todo.id == todo_id:
            todo_list[index] = updated
            return {"message": "To-Do updated"}
    raise HTTPException(status_code=404, detail="To-Do not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(todo_list):
        if todo.id == todo_id:
            del todo_list[index]
            return {"message": "To-Do deleted"}
    raise HTTPException(status_code=404, detail="To-Do not found")
