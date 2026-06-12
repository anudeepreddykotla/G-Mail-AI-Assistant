from app.auth.credential_manager import (
    get_valid_credentials
)

from app.gmail.gmail_service import (
    get_gmail_service
)


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

    return get_gmail_service(
        credentials
    )