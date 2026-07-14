from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel

class Role(str, Enum):  # These are the only 4 allowed roles
    owner = "owner"
    maintainer = "maintainer"
    member = "member"
    viewer = "viewer"

class TeamMembership(SQLModel, table=True):
    __tablename__= "team_memberships"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    team_id: int = Field(foreign_key="team.id")
    role: Role = Role.member 