from sqlalchemy import Column, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base import Base


class EmailAIMetadata(Base):
    __tablename__ = "email_ai_metadata"

    message_id = Column(Text, primary_key=True)
    thread_id = Column(Text, nullable=False, index=True)

    summary = Column(Text)
    intent = Column(String(64), index=True)
    priority = Column(String(16), index=True)

    labels = Column(JSONB)
    reminders = Column(JSONB)

    ai_model = Column(String(64), nullable=False)

    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(),
                        nullable=False)

    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(),
                        onupdate=func.now(),
                        nullable=False)