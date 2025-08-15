from typing import Optional
from sqlmodel import SQLModel, Field

class ToDo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task: str
    completed: bool = False
