from functools import lru_cache

from app.auth.credential_manager import (
    get_valid_credentials
)

from app.gmail.gmail_service import (
    get_gmail_service
)


@lru_cache(maxsize=20)
def _cached_service(email: str, token: str):
    return token


def get_gmail_client(
    db,
    email: str
):
    credentials = get_valid_credentials(
        db,
        email
    )

    if credentials is None:
        return None

    _cached_service(
        email,
        credentials.token
    )

    return get_gmail_service(
        credentials
    )