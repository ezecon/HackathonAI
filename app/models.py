from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    Text,
    ForeignKey
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

import uuid
from app.database import Base


# =========================
# 👤 USER MODEL
# =========================
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    class_level = Column(Integer, nullable=False)

    # 🧠 personalization (for AI)
    preferred_environment = Column(String, nullable=True)  # cricket, football etc
    total_attempts = Column(Integer, default=0)
    accuracy = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


# =========================
# 📚 RAG KNOWLEDGE BASE
# =========================
class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    topic = Column(
        String,
        index=True
    )

    class_level = Column(
        Integer,
        index=True
    )

    concept = Column(Text)

    explanation = Column(Text)

    example = Column(Text)

    embedding = Column(
        Text,
        nullable=True
    )

# =========================
# 📊 STUDENT PERFORMANCE
# =========================
class StudentPerformance(Base):
    __tablename__ = "student_performance"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(UUID(as_uuid=True), nullable=False)

    topic = Column(String, index=True)

    correct_count = Column(Integer, default=0)
    wrong_count = Column(Integer, default=0)

    accuracy = Column(Integer, default=0)

    last_updated = Column(DateTime(timezone=True), server_default=func.now())

class StudentGamification(Base):

    __tablename__ = "student_gamification"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    xp = Column(
        Integer,
        default=0
    )

    level = Column(
        Integer,
        default=1
    )

    streak_days = Column(
        Integer,
        default=0
    )

    badges = Column(
        Text,
        nullable=True
    )

    last_activity = Column(
        DateTime,
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    # ফাইলের শেষে যোগ করো
class QuestionHistory(Base):
    __tablename__ = "question_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)

    topic = Column(String, nullable=False)
    environment = Column(String, nullable=True)
    class_level = Column(Integer, nullable=False)

    question = Column(Text, nullable=False)      # word_problem
    correct_answer = Column(Text, nullable=True)  # answer
    student_answer = Column(Text, nullable=True)  # student যা লিখেছে
    is_correct = Column(String, nullable=True)    # 'true' / 'false' / 'pending'

    full_content = Column(Text, nullable=True)    # পুরো AI response (JSON)

    created_at = Column(DateTime(timezone=True), server_default=func.now())