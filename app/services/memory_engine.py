from sqlalchemy import text
from app.database import SessionLocal
from app.models import User, StudentPerformance
from app.services.performance_engine import get_weak_topics


def update_memory(user_id: str):

    db = SessionLocal()

    # =========================
    # USER INFO
    # =========================
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    preferred_environment = (
        user.preferred_environment
        if user and user.preferred_environment
        else "General"
    )

    # =========================
    # LAST TOPIC
    # =========================
    latest = db.query(StudentPerformance).filter(
        StudentPerformance.user_id == user_id
    ).order_by(
        StudentPerformance.last_updated.desc()
    ).first()

    last_topic = (
        latest.topic
        if latest
        else "Not Started"
    )

    # =========================
    # WEAK TOPICS
    # =========================
    weak_topics_data = get_weak_topics(user_id)

    weak_topics = []

    if weak_topics_data:

        for t in weak_topics_data:

            if isinstance(t, dict):
                weak_topics.append(
                    t.get("topic")
                )

            else:
                weak_topics.append(t)

    weak_topics = [
        w for w in weak_topics if w
    ]

    # =========================
    # STRONG TOPICS
    # =========================
    strong_rows = db.query(
        StudentPerformance
    ).filter(
        StudentPerformance.user_id == user_id,
        StudentPerformance.accuracy >= 70
    ).all()

    strong_topics = [
        row.topic
        for row in strong_rows
        if row.topic
    ]

    # =========================
    # MEMORY EXISTS?
    # =========================
    memory = db.execute(
        text("""
            select *
            from user_memory
            where user_id=:uid
        """),
        {
            "uid": user_id
        }
    ).fetchone()

    # =========================
    # UPDATE
    # =========================
    if memory:

        db.execute(
            text("""
                update user_memory
                set preferred_environment=:env,
                    last_topic=:topic,
                    weak_topics=:weak,
                    strong_topics=:strong,
                    updated_at=now()
                where user_id=:uid
            """),
            {
                "env": preferred_environment,
                "topic": last_topic,
                "weak": ",".join(weak_topics)
                if weak_topics else None,
                "strong": ",".join(strong_topics)
                if strong_topics else None,
                "uid": user_id
            }
        )

    # =========================
    # INSERT
    # =========================
    else:

        db.execute(
            text("""
                insert into user_memory
                (
                    user_id,
                    preferred_environment,
                    last_topic,
                    weak_topics,
                    strong_topics
                )
                values
                (
                    :uid,
                    :env,
                    :topic,
                    :weak,
                    :strong
                )
            """),
            {
                "uid": user_id,
                "env": preferred_environment,
                "topic": last_topic,
                "weak": ",".join(weak_topics)
                if weak_topics else None,
                "strong": ",".join(strong_topics)
                if strong_topics else None
            }
        )

    db.commit()
    db.close()

    return {
        "user_id": user_id,
        "preferred_environment": preferred_environment,
        "last_topic": last_topic,
        "weak_topics": weak_topics,
        "strong_topics": strong_topics
    }


# ==================================
# GET MEMORY FOR AI ENGINE
# ==================================
def get_user_memory(user_id):

    db = SessionLocal()

    row = db.execute(
        text("""
            select *
            from user_memory
            where user_id=:uid
        """),
        {
            "uid": user_id
        }
    ).mappings().fetchone()

    db.close()

    if not row:
        return None

    return dict(row)