import json

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from app.auth.token_repository import (
    get_tokens,
    get_decrypted_refresh_token,
    update_access_token
)

CLIENT_SECRETS_FILE = "app/auth/credentials.json"


def get_client_config():

    with open(
        CLIENT_SECRETS_FILE,
        "r"
    ) as file:

        config = json.load(file)

    return config["web"]


def get_valid_credentials(
    db,
    email: str
):

    token = get_tokens(
        db,
        email
    )

    if token is None:
        return None

    config = get_client_config()

    refresh_token = (
        get_decrypted_refresh_token(
            db,
            email
        )
    )

    credentials = Credentials(
        token=token.access_token,
        refresh_token=refresh_token,
        token_uri=config["token_uri"],
        client_id=config["client_id"],
        client_secret=config["client_secret"]
    )

    credentials.expiry = token.expires_at

    if credentials.expired:

        credentials.refresh(
            Request()
        )

        update_access_token(
            db=db,
            email=email,
            access_token=credentials.token,
            expires_at=credentials.expiry
        )

    return credentials