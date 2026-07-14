from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel

class ActivityLog(SQLModel, table=True):
    __tablename__= "activity_logs"
    id: Optional[int] = Field(default=None, primary_key=True)
    action: str  
    user_id: int = Field(foreign_key="user.id")
    team_id: int = Field(foreign_key="team.id")
    default_factory=lambda: datetime.now(timezone.utc)