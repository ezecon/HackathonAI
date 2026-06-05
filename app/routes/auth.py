from fastapi import (
    APIRouter,
    Depends
)

from app.dependencies.auth import (
    get_current_user
)

from app.services.user_sync import (
    sync_user
)

from app.services.gamification_engine import (
    get_user_gamification
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.get("/me")
def me(
    current_user=Depends(
        get_current_user
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

    gamification = (
        get_user_gamification(
            user_id
        )
    )

    return {

        "user": {
            "id":
            user_id,

            "email":
            current_user[
                "email"
            ],

            "name":
            current_user[
                "name"
            ]
        },

        "gamification":
        gamification
    }