from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel

class Comment(SQLModel, table=True):
    __tablename__= "comments"
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    task_id: int = Field(foreign_key="tasks.id")
    user_id: int = Field(foreign_key="users.id")
    default_factory=lambda: datetime.now(timezone.utc)