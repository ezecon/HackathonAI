from datetime import datetime

from sqlalchemy import text

from app.database import SessionLocal
from sqlalchemy import text
from app.database import SessionLocal


def get_user_gamification(
    user_id: str
):

    db = SessionLocal()

    result = db.execute(
        text("""
            SELECT *
            FROM student_gamification
            WHERE user_id=:uid
        """),
        {
            "uid": user_id
        }
    ).mappings().fetchone()

    db.close()

    return dict(result) if result else None


def update_gamification(
    user_id: str,
    is_correct: bool
):

    db = SessionLocal()

    gamification = db.execute(
        text("""
            select *
            from student_gamification
            where user_id=:uid
        """),
        {"uid": user_id}
    ).mappings().fetchone()

    xp_gain = 10 if is_correct else 2

    # FIRST ENTRY
    if not gamification:

        db.execute(text("""
            insert into student_gamification
            (
                user_id,
                xp,
                level,
                streak_days,
                last_activity
            )
            values
            (
                :uid,
                :xp,
                1,
                1,
                now()
            )
        """), {
            "uid": user_id,
            "xp": xp_gain
        })

    else:

        xp = gamification["xp"] + xp_gain

        level = (xp // 100) + 1

        streak = gamification[
            "streak_days"
        ]

        last_activity = gamification[
            "last_activity"
        ]

        today = datetime.utcnow().date()

        if last_activity:

            difference = (
                today -
                last_activity.date()
            ).days

            if difference == 1:
                streak += 1

            elif difference > 1:
                streak = 1

        db.execute(text("""
            update student_gamification
            set xp=:xp,
                level=:level,
                streak_days=:streak,
                last_activity=now(),
                updated_at=now()
            where user_id=:uid
        """), {

            "xp": xp,
            "level": level,
            "streak": streak,
            "uid": user_id
        })

    db.commit()

    result = db.execute(
        text("""
            select *
            from student_gamification
            where user_id=:uid
        """),
        {"uid": user_id}
    ).mappings().fetchone()

    db.close()

    return dict(result)