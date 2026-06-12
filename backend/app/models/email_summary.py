from sqlalchemy import Column, Integer, String, Text

from app.db.base import Base


class EmailSummaryCache(Base):
    __tablename__ = "email_summary_cache"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    message_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    short_summary = Column(
        Text,
        nullable=False
    )

    bullet_points = Column(
        Text,
        nullable=False
    )

    action_items = Column(
        Text,
        nullable=False
    )