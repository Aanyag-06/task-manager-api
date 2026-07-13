from pydantic import BaseModel

class CommentCreate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    content: str
    task_id: int
    user_id: int

    class Config:
        from_attributes = True