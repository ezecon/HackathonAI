from sqlalchemy import text
from app.database import SessionLocal


def detect_misconception(
    topic: str
):

    # Phase 8.1
    # Rule Based Version

    if topic == "Fractions":

        return "Fraction Concept Error"

    elif topic == "Ratio":

        return "Ratio Interpretation Error"

    elif topic == "Percentage":

        return "Percentage Calculation Error"

    return "General Concept Error"


def save_misconception(
    user_id: str,
    topic: str,
    misconception: str
):

    db = SessionLocal()

    existing = db.execute(
        text("""
            select *
            from student_misconceptions
            where user_id=:uid
            and topic=:topic
            and misconception=:m
        """),
        {
            "uid": user_id,
            "topic": topic,
            "m": misconception
        }
    ).mappings().fetchone()

    # --------------------
    # UPDATE EXISTING
    # --------------------
    if existing:

        db.execute(
            text("""
                update student_misconceptions
                set count=count+1,
                    last_seen=now()
                where id=:id
            """),
            {
                "id": existing["id"]
            }
        )

    # --------------------
    # INSERT NEW
    # --------------------
    else:

        db.execute(
            text("""
                insert into
                student_misconceptions
                (
                    user_id,
                    topic,
                    misconception
                )
                values
                (
                    :uid,
                    :topic,
                    :m
                )
            """),
            {
                "uid": user_id,
                "topic": topic,
                "m": misconception
            }
        )

    db.commit()
    db.close()


def get_user_misconceptions(
    user_id: str
):

    db = SessionLocal()

    rows = db.execute(
        text("""
            select *
            from student_misconceptions
            where user_id=:uid
            order by count desc
        """),
        {
            "uid": user_id
        }
    ).mappings().all()

    db.close()

    return [dict(row) for row in rows]