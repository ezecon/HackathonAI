from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import json

from ..database import SessionLocal
from ..schemas import QuestionHistorySave
from ..dependencies.auth import get_current_user
from ..models import QuestionHistory

router = APIRouter(prefix="/history", tags=["History"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================
# SAVE QUESTION
# ==========================
@router.post("/save")
def save_question(
    data: QuestionHistorySave,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user["user_id"]

    record = QuestionHistory(
        user_id=user_id,
        topic=data.topic,
        environment=data.environment,
        class_level=data.class_level,
        question=data.question,
        correct_answer=data.correct_answer,
        student_answer=data.student_answer,
        is_correct=data.is_correct,
        full_content=data.full_content,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return {"message": "Saved", "id": str(record.id)}


# ==========================
# UPDATE RESULT (after submit)
# ==========================
@router.patch("/update/{history_id}")
def update_result(
    history_id: str,
    student_answer: str,
    is_correct: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    import uuid
    record = db.query(QuestionHistory).filter(
        QuestionHistory.id == uuid.UUID(history_id),
        QuestionHistory.user_id == current_user["user_id"]
    ).first()

    if not record:
        return {"error": "Not found"}

    record.student_answer = student_answer
    record.is_correct = is_correct
    db.commit()

    return {"message": "Updated"}


# ==========================
# GET HISTORY
# ==========================
@router.get("/{user_id}")
def get_history(
    user_id: str,
    limit: int = 20,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user_id != current_user["user_id"]:
        return {"error": "Unauthorized"}

    records = db.query(QuestionHistory).filter(
        QuestionHistory.user_id == user_id
    ).order_by(
        QuestionHistory.created_at.desc()
    ).limit(limit).all()

    return [
        {
            "id": str(r.id),
            "topic": r.topic,
            "environment": r.environment,
            "class_level": r.class_level,
            "question": r.question,
            "correct_answer": r.correct_answer,
            "student_answer": r.student_answer,
            "is_correct": r.is_correct,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in records
    ]