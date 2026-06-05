from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.memory_retriever import (
    get_user_memory
)
from app.services.gamification_engine import (
    update_gamification
)
from app.database import SessionLocal
from app.schemas import AnswerSubmission

from app.dependencies.auth import (
    get_current_user
)
from app.crud import update_student_performance

from app.services.performance_engine import (
    get_weak_topics
)
from app.services.badge_engine import (
    update_badges
)
from app.services.memory_engine import (
    update_memory
)
from app.services.leaderboard_engine import (
    get_leaderboard
)
from app.services.misconception_engine import (
    detect_misconception,
    save_misconception
)
from app.dependencies.auth import (
    get_current_user
)

from app.services.user_sync import (
    sync_user
)
from app.services.recommendation_engine import (
    generate_recommendation
)
from app.services.remediation_engine import (
    generate_remediation
)

from app.services.analytics_engine import (
    get_student_analytics
)

from app.services.mastery_engine import (
    calculate_mastery_score
)

router = APIRouter(
    prefix="/performance",
    tags=["Performance"]
)


# ==========================
# DB
# ==========================
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ==========================
# WEAK TOPICS
# ==========================
@router.get(
    "/weak-topics/{user_id}"
)
def weak_topics(
    user_id: str,
    current_user=Depends(
        get_current_user
    )
):

    if user_id != current_user[
        "user_id"
    ]:
        return {
            "error":
            "Unauthorized"
        }

    return get_weak_topics(
        user_id
    )
# ==========================
# SUBMIT ANSWER
# ==========================
@router.post(
    "/submit"
)
def submit_answer(
    data: AnswerSubmission,
    current_user=Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):

    user_id = current_user[
        "user_id"
    ]

    sync_user(
        user_id=user_id,
        email=current_user[
            "email"
        ],
        name=current_user[
            "name"
        ]
    )

    result = update_student_performance(
        db,
        user_id,
        data.topic,
        data.is_correct
    )

    memory = update_memory(
        user_id
    )

    misconception = None

    if not data.is_correct:

        misconception = (
            detect_misconception(
                data.topic
            )
        )

        save_misconception(
            user_id,
            data.topic,
            misconception
        )

    gamification = (
        update_gamification(
            user_id,
            data.is_correct
        )
    )

    gamification = (
        update_badges(
            user_id
        )
    )

    return {

        "performance": {
            "topic":
            result.topic,

            "correct_count":
            result.correct_count,

            "wrong_count":
            result.wrong_count,

            "accuracy":
            result.accuracy
        },

        "memory":
        memory,

        "gamification":
        gamification,

        "misconception":
        misconception,

        "message":
        "Performance updated successfully"
    }


# ==========================
# RECOMMENDATION
# ==========================
@router.get(
    "/recommendation/{user_id}/{class_level}"
)
def recommendation(
    user_id: str,
    class_level: int,
    current_user=Depends(
        get_current_user
    )
):

    if user_id != current_user[
        "user_id"
    ]:
        return {
            "error":
            "Unauthorized"
        }

    return generate_recommendation(
        user_id,
        class_level
    )
# ==========================
# REMEDIATION
# ==========================

@router.get(
    "/remediation/{user_id}/{class_level}"
)
def remediation(
    user_id: str,
    class_level: int,
    current_user=Depends(
        get_current_user
    )
):

    if user_id != current_user[
        "user_id"
    ]:
        return {
            "error":
            "Unauthorized"
        }

    recommendation_data = generate_recommendation(
        user_id,
        class_level
    )

    memory = get_user_memory(
        user_id
    )

    environment = "general"

    if memory:
        environment = memory.get(
            "preferred_environment",
            "general"
        )

    return generate_remediation(
        user_id=user_id,
        topic=recommendation_data.get(
            "topic",
            "Ratio"
        ),
        score=0,
        environment=environment,
        class_level=class_level
    )
# ==========================
# ANALYTICS
# ==========================
@router.get(
    "/analytics/{user_id}"
)
def analytics(
    user_id: str,
    current_user=Depends(
        get_current_user
    )
):

    if user_id != current_user[
        "user_id"
    ]:
        return {
            "error":
            "Unauthorized"
        }

    return get_student_analytics(
        user_id
    )


# ==========================
# MASTERY
# ==========================
@router.get(
    "/mastery/{user_id}"
)
def mastery(
    user_id: str,
    current_user=Depends(
        get_current_user
    )
):

    if user_id != current_user[
        "user_id"
    ]:
        return {
            "error":
            "Unauthorized"
        }
    return calculate_mastery_score(
        user_id
    )

@router.get(
    "/leaderboard"
)
def leaderboard():

    return get_leaderboard()

