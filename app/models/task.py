from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel

class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Task(SQLModel, table=True):
    __tablename__= "tasks"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.medium
    project_id: int = Field(foreign_key="projects.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TaskAssignment(SQLModel, table=True):  # Handles many users working on one task
    __tablename__="task_assignments"
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="tasks.id")
    user_id: int = Field(foreign_key="users.id")