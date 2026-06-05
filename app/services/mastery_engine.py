from sqlalchemy import text
from app.database import SessionLocal


def calculate_mastery_score(user_id: str):

    db = SessionLocal()

    performance = db.execute(
        text("""
            select *
            from student_performance
            where user_id=:uid
        """),
        {"uid": user_id}
    ).mappings().all()

    misconceptions = db.execute(
        text("""
            select *
            from student_misconceptions
            where user_id=:uid
        """),
        {"uid": user_id}
    ).mappings().all()

    memory = db.execute(
        text("""
            select *
            from user_memory
            where user_id=:uid
        """),
        {"uid": user_id}
    ).mappings().fetchone()

    db.close()

    if not performance:
        return {
            "mastery_score": 0,
            "level": "Beginner"
        }

    avg_accuracy = sum(
        p["accuracy"] for p in performance
    ) / len(performance)

    strong_count = 0
    weak_count = 0

    if memory:
        strong_count = len(
            memory["strong_topics"].split(",")
        ) if memory["strong_topics"] else 0

        weak_count = len(
            memory["weak_topics"].split(",")
        ) if memory["weak_topics"] else 0

    misconception_penalty = len(misconceptions) * 5

    score = (
        avg_accuracy +
        (strong_count * 10) -
        (weak_count * 5) -
        misconception_penalty
    )

    score = max(0, min(100, round(score)))

    if score >= 80:
        level = "Advanced"
    elif score >= 60:
        level = "Intermediate"
    else:
        level = "Beginner"

    return {
        "mastery_score": score,
        "level": level
    }