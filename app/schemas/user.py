from pydantic import BaseModel, EmailStr

# what the user sends when signing up
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# what you send back 
class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

# what the user sends when logging in
class LoginRequest(BaseModel):
    email: str
    password: str