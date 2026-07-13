from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password: str  # This will store a hashed password, never plain text!
    created_at: datetime = Field(default_factory=datetime.utcnow)