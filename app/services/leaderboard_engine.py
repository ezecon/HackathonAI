from sqlalchemy import text

from app.database import SessionLocal


def get_leaderboard():

    db = SessionLocal()

    rows = db.execute(
        text("""
            select
                u.name,
                g.xp,
                g.level,
                g.badges
            from student_gamification g
            join users u
            on g.user_id = u.id
            order by g.xp desc
            limit 10
        """)
    ).mappings().fetchall()

    db.close()

    return [
        dict(row)
        for row in rows
    ]