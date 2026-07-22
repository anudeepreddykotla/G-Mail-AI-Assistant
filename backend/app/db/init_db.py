from sqlalchemy import text

from app.db.database import engine
from app.db.base import Base

from app.models.user import User
from app.models.oauth_session import OAuthSession
from app.models.oauth_token import OAuthToken
from app.models.email_summary import EmailSummaryCache
from app.models.email_ai_metadata import EmailAIMetadata
from app.models.email_embedding import EmailEmbedding

with engine.begin() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))

Base.metadata.create_all(bind=engine)

print("Database initialized")