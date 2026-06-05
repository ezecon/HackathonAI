from fastapi import (
    Header,
    HTTPException
)

from app.core.auth import (
    verify_token
)


def get_current_user(
    authorization: str = Header(None)
):

    if not authorization:

        raise HTTPException(
            status_code=401,
            detail="Missing token"
        )

    token = authorization.replace(
        "Bearer ",
        ""
    )

    user = verify_token(
        token
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return {

        "user_id":
        user["id"],

        "email":
        user["email"],

        "name":
        user.get(
            "user_metadata",
            {}
        ).get(
            "full_name",
            "Unknown"
        )
    }