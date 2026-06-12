from fastapi import Depends
from fastapi import HTTPException

from app.db.session import get_db

from sqlalchemy.orm import Session

from app.auth.current_user import (
    get_current_user
)

from app.models.user import User

from app.gmail.gmail_client import (
    get_gmail_client
)


def get_current_gmail(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    gmail = get_gmail_client(
        db,
        current_user.email
    )

    if gmail is None:

        raise HTTPException(
            status_code=401,
            detail="Gmail account not connected"
        )

    return gmail