from google import genai
from google.genai import types

from app.core.config import settings


class EmbeddingService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = "gemini-embedding-001"

    def generate_embedding(self, text: str) -> list[float]:
        if not text.strip():
            return [0.0] * 768

        response = self.client.models.embed_content(
            model=self.model,
            contents=text,
            config=types.EmbedContentConfig(
                output_dimensionality=768
            ),
        )

        return response.embeddings[0].values


embedding_service = EmbeddingService()