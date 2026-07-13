from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    task_id: int = Field(foreign_key="task.id")
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)