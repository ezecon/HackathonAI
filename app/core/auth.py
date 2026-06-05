import os
import requests

from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv(
    "SUPABASE_URL"
)

SUPABASE_ANON_KEY = os.getenv(
    "SUPABASE_ANON_KEY"
)


def verify_token(
    token: str
):

    response = requests.get(
        f"{SUPABASE_URL}/auth/v1/user",
        headers={
            "apikey":
            SUPABASE_ANON_KEY,

            "Authorization":
            f"Bearer {token}"
        }
    )

    if response.status_code != 200:
        return None

    return response.json()