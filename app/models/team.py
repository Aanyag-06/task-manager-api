from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    owner_id: int = Field(foreign_key="user.id")  # This links this team to a User ID
    created_at: datetime = Field(default_factory=datetime.utcnow)