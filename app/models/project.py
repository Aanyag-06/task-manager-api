from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    team_id: int = Field(foreign_key="team.id")  # Links project to a specific team
    created_at: datetime = Field(default_factory=datetime.utcnow)