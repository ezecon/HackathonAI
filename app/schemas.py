from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: str
    class_level: int
    preferred_environment: Optional[str] = "General"


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    class_level: int
    preferred_environment: Optional[str]

    class Config:
        from_attributes = True


class AnswerSubmission(BaseModel):
    topic: str
    is_correct: bool

class AIRequest(BaseModel):
    user_id: str
    topic: str
    environment: str
    class_level: int