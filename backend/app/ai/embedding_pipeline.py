from sqlalchemy.orm import Session

from app.ai.embedding import embedding_service
from app.ai.resolver import AIContentResolver
from app.ai.schemas import EmbeddingResponse
from app.ai.utils import clean_email_body
from app.ai.vector_store import save_embedding


def generate_and_store_embedding(
    db: Session,
    gmail,
    message_id: str,
) -> EmbeddingResponse:
    content = AIContentResolver.resolve_message(
        gmail,
        message_id,
    )

    content = clean_email_body(content)

    embedding = embedding_service.generate_embedding(content)

    save_embedding(
        db=db,
        message_id=message_id,
        embedding=embedding,
        model=embedding_service.model,
    )

    return EmbeddingResponse(
        success=True,
        message_id=message_id,
        dimensions=len(embedding),
    )