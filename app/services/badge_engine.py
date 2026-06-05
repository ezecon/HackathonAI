from sqlalchemy import text

from app.database import SessionLocal


def update_badges(
    user_id: str
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

    if not gamification:

        db.close()

        return []

    badges = []

    existing_badges = gamification[
        "badges"
    ]

    if existing_badges:

        badges = existing_badges.split(
            ","
        )

    xp = gamification["xp"]

    streak = gamification[
        "streak_days"
    ]

    # -------------------------
    # XP BADGES
    # -------------------------
    if "Beginner" not in badges:
        badges.append(
            "Beginner"
        )

    if xp >= 10 and \
       "Quick Learner" not in badges:

        badges.append(
            "Quick Learner"
        )

    if xp >= 50 and \
       "Rising Star" not in badges:

        badges.append(
            "Rising Star"
        )

    if xp >= 100 and \
       "Math Warrior" not in badges:

        badges.append(
            "Math Warrior"
        )

    # -------------------------
    # STREAK BADGES
    # -------------------------
    if streak >= 3 and \
       "Consistent Learner" not in badges:

        badges.append(
            "Consistent Learner"
        )

    if streak >= 7 and \
       "Study Champion" not in badges:

        badges.append(
            "Study Champion"
        )

    # -------------------------
    # SAVE
    # -------------------------
    db.execute(text("""
        update student_gamification
        set badges=:badges,
            updated_at=now()
        where user_id=:uid
    """), {

        "badges":
        ",".join(badges),

        "uid":
        user_id
    })

    db.commit()

    final_result = db.execute(
        text("""
            select *
            from student_gamification
            where user_id=:uid
        """),
        {"uid": user_id}
    ).mappings().fetchone()

    db.close()

    return dict(final_result)