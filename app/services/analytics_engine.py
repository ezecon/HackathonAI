from sqlalchemy import text
from app.database import SessionLocal


def get_student_analytics(
    user_id: str
):

    db = SessionLocal()

    performance = db.execute(
        text("""
            select *
            from student_performance
            where user_id=:uid
        """),
        {
            "uid": user_id
        }
    ).mappings().all()

    misconceptions = db.execute(
        text("""
            select *
            from student_misconceptions
            where user_id=:uid
        """),
        {
            "uid": user_id
        }
    ).mappings().all()

    memory = db.execute(
        text("""
            select *
            from user_memory
            where user_id=:uid
        """),
        {
            "uid": user_id
        }
    ).mappings().fetchone()

    total_topics = len(performance)

    avg_accuracy = 0

    if performance:

        avg_accuracy = round(
            sum(
                p["accuracy"]
                for p in performance
            ) / len(performance),
            2
        )

    strong_topics = []
    weak_topics = []

    if memory:

        strong_topics = (
            memory["strong_topics"].split(",")
            if memory["strong_topics"]
            else []
        )

        weak_topics = (
            memory["weak_topics"].split(",")
            if memory["weak_topics"]
            else []
        )

    most_common_misconception = None

    if misconceptions:

        sorted_data = sorted(
            misconceptions,
            key=lambda x: x["count"],
            reverse=True
        )

        most_common_misconception = sorted_data[0]["misconception"]

    db.close()

    return {

        "total_topics_attempted":
        total_topics,

        "average_accuracy":
        avg_accuracy,

        "strong_topics":
        strong_topics,

        "weak_topics":
        weak_topics,

        "total_misconceptions":
        len(misconceptions),

        "most_common_misconception":
        most_common_misconception,

        "last_topic":
        memory["last_topic"] if memory else None
    }