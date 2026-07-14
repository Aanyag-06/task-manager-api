from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel

class Team(SQLModel, table=True):
    __tablename__= "teams"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    owner_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))