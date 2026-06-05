from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate
from app.models import StudentPerformance


def update_student_performance(
    db,
    user_id,
    topic,
    is_correct
):

    record = db.query(
        StudentPerformance
    ).filter(
        StudentPerformance.user_id == user_id,
        StudentPerformance.topic == topic
    ).first()

    if not record:

        record = StudentPerformance(
            user_id=user_id,
            topic=topic,
            correct_count=0,
            wrong_count=0,
            accuracy=0
        )

        db.add(record)

    if is_correct:
        record.correct_count += 1
    else:
        record.wrong_count += 1

    total = (
        record.correct_count +
        record.wrong_count
    )

    record.accuracy = int(
        (record.correct_count / total) * 100
    )

    db.commit()
    db.refresh(record)

    return record

# CREATE USER
def create_user(db: Session, user: UserCreate):

    new_user = User(
        name=user.name,
        email=user.email,
        class_level=user.class_level,
        preferred_environment=user.preferred_environment
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
# GET ALL USERS
def get_users(db: Session):
    return db.query(User).all()

# GET USER BY ID
def get_user(db: Session, user_id):
    return db.query(User).filter(User.id == user_id).first()

# DELETE USER
def delete_user(db: Session, user_id):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user