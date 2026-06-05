from fastapi import APIRouter
from fastapi import Depends

from app.dependencies.auth import (
    get_current_user
)
from app.schemas import AIRequest

from app.services.ai_engine import (
    generate_learning_content
)

router = APIRouter()


@router.post(
    "/generate"
)
def generate(
    request: AIRequest,
    current_user=Depends(
        get_current_user
    )
):

    result = generate_learning_content(
        user_id=current_user["user_id"],
        topic=request.topic,
        environment=request.environment,
        class_level=request.class_level
    )

    return {
        "content": result
    }