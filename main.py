from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from models import ToDo
from database import create_db_and_tables, get_session

app = FastAPI()

# 🟢 Automatically create the database & table on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# ✅ Add a new To-Do
@app.post("/todos/", response_model=ToDo)
def create_todo(todo: ToDo, session: Session = Depends(get_session)):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

# 📋 Get all To-Dos
@app.get("/todos/", response_model=list[ToDo])
def read_todos(session: Session = Depends(get_session)):
    todos = session.exec(select(ToDo)).all()
    return todos

# 🔍 Get a single To-Do by ID
@app.get("/todos/{todo_id}", response_model=ToDo)
def read_todo(todo_id: int, session: Session = Depends(get_session)):
    todo = session.get(ToDo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo not found")
    return todo

# ✏️ Update a To-Do
@app.put("/todos/{todo_id}", response_model=ToDo)
def update_todo(todo_id: int, updated: ToDo, session: Session = Depends(get_session)):
    db_todo = session.get(ToDo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="ToDo not found")
    db_todo.task = updated.task
    db_todo.completed = updated.completed
    session.commit()
    session.refresh(db_todo)
    return db_todo

# ❌ Delete a To-Do
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, session: Session = Depends(get_session)):
    todo = session.get(ToDo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo not found")
    session.delete(todo)
    session.commit()
    return {"message": "ToDo deleted"}
