from datetime import datetime

from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base


class OAuthToken(Base):

    __tablename__ = "oauth_tokens"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    gmail_email: Mapped[str] = mapped_column(
        String
    )

    access_token: Mapped[str] = mapped_column(
        String
    )

    refresh_token: Mapped[str] = mapped_column(
        String
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )