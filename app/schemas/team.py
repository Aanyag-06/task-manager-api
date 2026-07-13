from pydantic import BaseModel
from app.models.membership import Role

# what you send when creating a team
class TeamCreate(BaseModel):
    name: str
    description: str | None = None

# what you send when inviting someone
class InviteMember(BaseModel):
    email: str
    role: Role = Role.member

# what you send when changing someone's role
class ChangeRole(BaseModel):
    email: str
    role: Role

# what gets sent back in responses
class TeamResponse(BaseModel):
    id: int
    name: str
    description: str | None
    owner_id: int

    class Config:
        from_attributes = True

class MemberResponse(BaseModel):
    user_id: int
    email: str
    role: Role