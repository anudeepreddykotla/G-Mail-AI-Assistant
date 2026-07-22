from sqlalchemy import Column, DateTime, String, Text, func
from pgvector.sqlalchemy import Vector

from app.db.base import Base


class EmailEmbedding(Base):
    __tablename__ = "email_embeddings"

    message_id = Column(Text, primary_key=True)

    embedding = Column(Vector(768), nullable=False)

    model = Column(String(64), nullable=False)

    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(),
                        nullable=False)