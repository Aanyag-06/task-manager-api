from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel

class ActivityLog(SQLModel, table=True):
    __tablename__ = "activity_logs"
    id: Optional[int] = Field(default=None, primary_key=True)
    action: str  
    user_id: int = Field(foreign_key="users.id")
    team_id: int = Field(foreign_key="teams.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))