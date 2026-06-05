from sqlalchemy import text

from app.database import (
    SessionLocal
)


def sync_user(
    user_id: str,
    email: str,
    name: str
):

    db = SessionLocal()

    existing_user = db.execute(
        text("""
            SELECT *
            FROM users
            WHERE id=:id
        """),
        {
            "id": user_id
        }
    ).fetchone()

    if not existing_user:

        db.execute(
            text("""
                INSERT INTO users
                (
                    id,
                    name,
                    email,
                    class_level,
                    preferred_environment
                )
                VALUES
                (
                    :id,
                    :name,
                    :email,
                    6,
                    'General'
                )
            """),
            {
                "id": user_id,
                "name": name,
                "email": email
            }
        )

        db.commit()

    db.close()