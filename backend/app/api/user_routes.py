from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.create_user_request import (
    CreateUserRequest
)

from app.gmail.user_service import (
    create_user,
    get_user_by_email
)

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("")
def create_new_user(
    request: CreateUserRequest,
    db: Session = Depends(get_db)
):

    existing = get_user_by_email(
        db,
        request.email
    )

    if existing:

        return {
            "error": "User already exists"
        }

    return create_user(
        db,
        request.email,
        request.name
    )

@router.get("/{email}")
def get_user(
    email: str,
    db: Session = Depends(get_db)
):

    return get_user_by_email(
        db,
        email
    )