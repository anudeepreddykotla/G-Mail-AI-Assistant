from datetime import datetime

from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime, timedelta

from app.db.base import Base


class OAuthSession(Base):

    __tablename__ = "oauth_sessions"

    state: Mapped[str] = mapped_column(
        String,
        primary_key=True
    )

    pkce_verifier: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )