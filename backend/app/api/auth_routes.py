from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends

from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.auth.pkce import generate_pkce

from app.auth.google_auth import (
    create_flow_with_pkce
)

from app.auth.oauth_repository import (
    create_oauth_session,
    get_oauth_session,
    delete_oauth_session
)

from app.auth.token_repository import (
    save_tokens
)

from app.gmail.gmail_service import (
    get_gmail_service
)

from app.gmail.user_service import (
    get_user_by_email,
    create_user
)

from app.auth.jwt_service import (
    create_access_token
)

from app.auth.current_user import (
    get_current_user
)

from app.models.user import User

router = APIRouter()


@router.get("/")
def home():

    return {
        "message": "Gmail AI Assistant"
    }


@router.get("/auth/login")
def login(
    db: Session = Depends(get_db)
):

    verifier, _ = generate_pkce()

    flow = create_flow_with_pkce(
        verifier
    )

    authorization_url, state = (
        flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true"
        )
    )

    create_oauth_session(
        db,
        state,
        verifier
    )

    return RedirectResponse(
        authorization_url
    )


@router.get("/auth/callback")
async def callback(
    request: Request,
    db: Session = Depends(get_db)
):

    state = request.query_params.get(
        "state"
    )

    oauth_session = get_oauth_session(
        db,
        state
    )

    if oauth_session is None:

        return {
            "error": "Invalid state"
        }

    flow = create_flow_with_pkce(
        oauth_session.pkce_verifier
    )

    flow.fetch_token(
        authorization_response=str(
            request.url
        )
    )

    credentials = flow.credentials

    gmail = get_gmail_service(
        credentials
    )

    profile = (
        gmail.users()
        .getProfile(
            userId="me"
        )
        .execute()
    )

    email = profile["emailAddress"]

    user = get_user_by_email(
        db,
        email
    )

    if user is None:

        user = create_user(
            db,
            email=email,
            name=email
        )

    save_tokens(
        db=db,
        email=email,
        access_token=credentials.token,
        refresh_token=credentials.refresh_token,
        expires_at=credentials.expiry
    )

    delete_oauth_session(
        db,
        state
    )

    jwt_token = create_access_token(
        user_id=user.id,
        email=user.email
    )

    return RedirectResponse(
        url=f"http://localhost:3000/auth/callback?token={jwt_token}"
    )

@router.get("/auth/me")
def get_me(
    current_user: User = Depends(
        get_current_user
    )
):

    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name
    }

@router.post("/auth/logout")
def logout():

    return {
        "success": True
    }