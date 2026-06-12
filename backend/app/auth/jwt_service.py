from datetime import datetime
from datetime import timedelta
from datetime import timezone

import jwt


SECRET_KEY = (
    "change-this-later"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(
    user_id: int,
    email: str
):

    expire = (
        datetime.now(
            timezone.utc
        )
        +
        timedelta(
            minutes=
            ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def verify_token(
    token: str
):

    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[
            ALGORITHM
        ]
    )