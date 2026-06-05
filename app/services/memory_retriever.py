from sqlalchemy import text
from app.database import SessionLocal


def get_user_memory(user_id):

    db = SessionLocal()

    row = db.execute(
        text("""
            select *
            from user_memory
            where user_id=:uid
        """),
        {"uid": user_id}
    ).mappings().fetchone()

    db.close()

    return dict(row) if row else None