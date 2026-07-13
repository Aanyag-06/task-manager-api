from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class ActivityLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    action: str  # e.g., "User X created task Y"
    user_id: int = Field(foreign_key="user.id")
    team_id: int = Field(foreign_key="team.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)