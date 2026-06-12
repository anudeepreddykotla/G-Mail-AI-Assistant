from dotenv import load_dotenv
import os

load_dotenv()


class Settings:

    DATABASE_URL = os.getenv("DATABASE_URL")

    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


settings = Settings()