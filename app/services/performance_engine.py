from app.database import SessionLocal
from app.models import StudentPerformance


def get_weak_topics(user_id):

    db = SessionLocal()

    rows = db.query(StudentPerformance).filter(
        StudentPerformance.user_id == user_id
    ).all()

    weak_topics = []

    for row in rows:
        if row.accuracy < 50:
            weak_topics.append({
                "topic": row.topic,
                "accuracy": row.accuracy
            })

    return weak_topics