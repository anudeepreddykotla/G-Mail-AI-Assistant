from sqlalchemy.orm import Session

from app.models.oauth_token import OAuthToken

from app.models.user import User

from app.security.encryption import (
    encrypt,
    decrypt
)

def save_tokens(
    db: Session,
    email: str,
    access_token: str,
    refresh_token: str | None,
    expires_at
):

    encrypted_refresh_token = None

    if refresh_token:

        encrypted_refresh_token = encrypt(
            refresh_token
        )

    existing = (
        db.query(OAuthToken)
        .filter(
            OAuthToken.gmail_email == email
        )
        .first()
    )

    if existing:

        existing.access_token = access_token

        if encrypted_refresh_token:

            existing.refresh_token = (
                encrypted_refresh_token
            )

        existing.expires_at = expires_at

    else:

        user = (
            db.query(User)
            .filter(
                User.email == email
            )
            .first()
        )

        if user is None:
            raise Exception(
                f"User not found: {email}"
            )

        token = OAuthToken(
            user_id=user.id,
            gmail_email=email,
            access_token=access_token,
            refresh_token=encrypted_refresh_token,
            expires_at=expires_at
        )

        db.add(token)

    db.commit()

    return True


def get_tokens(
    db,
    email: str
):

    return (
        db.query(OAuthToken)
        .filter(
            OAuthToken.gmail_email == email
        )
        .first()
    )


def update_access_token(
    db,
    email: str,
    access_token: str,
    expires_at
):

    token = (
        db.query(OAuthToken)
        .filter(
            OAuthToken.gmail_email == email
        )
        .first()
    )

    if token:

        token.access_token = access_token
        token.expires_at = expires_at

        db.commit()

    return token

def get_decrypted_refresh_token(
    db: Session,
    email: str
):

    token = (
        db.query(OAuthToken)
        .filter(
            OAuthToken.gmail_email == email
        )
        .first()
    )

    if token is None:
        return None

    if token.refresh_token is None:
        return None

    return decrypt(
        token.refresh_token
    )