from sqlalchemy.orm import Session

from app.models.oauth_session import OAuthSession


def create_oauth_session(
    db: Session,
    state: str,
    pkce_verifier: str
):

    session = OAuthSession(
        state=state,
        pkce_verifier=pkce_verifier
    )

    db.add(session)
    db.commit()

    return session


def get_oauth_session(
    db: Session,
    state: str
):

    return (
        db.query(OAuthSession)
        .filter(
            OAuthSession.state == state
        )
        .first()
    )


def delete_oauth_session(
    db: Session,
    state: str
):

    session = (
        db.query(OAuthSession)
        .filter(
            OAuthSession.state == state
        )
        .first()
    )

    if session:

        db.delete(session)
        db.commit()