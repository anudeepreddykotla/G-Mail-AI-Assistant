from app.db.database import engine

from app.db.base import Base

from app.models.user import User
from app.models.oauth_session import OAuthSession
from app.models.oauth_token import OAuthToken
from app.models.email_summary import EmailSummaryCache

Base.metadata.create_all(bind=engine)

print("Database initialized")