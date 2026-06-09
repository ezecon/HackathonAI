from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from typing import Optional
from datetime import datetime

class QuestionHistorySave(BaseModel):
    topic: str
    environment: str
    class_level: int
    question: str
    correct_answer: Optional[str] = None
    student_answer: Optional[str] = None
    is_correct: Optional[str] = "pending"
    full_content: Optional[str] = None

class QuestionHistoryResponse(BaseModel):
    id: str
    topic: str
    environment: Optional[str]
    class_level: int
    question: str
    correct_answer: Optional[str]
    student_answer: Optional[str]
    is_correct: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

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
    language: str = "en"