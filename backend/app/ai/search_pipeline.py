from sqlalchemy.orm import Session

from app.ai.embedding import embedding_service
from app.ai.schemas import (
    SemanticSearchResponse,
    SemanticSearchResult,
)
from app.ai.vector_store import search_similar
from app.gmail.message_service import get_message_by_id


def semantic_search(
    db: Session,
    gmail,
    query: str,
    limit: int,
) -> SemanticSearchResponse:

    embedding = embedding_service.generate_embedding(query)

    matches = search_similar(
        db=db,
        embedding=embedding,
        limit=limit,
    )

    results = []

    for match in matches:
        message = get_message_by_id(
            gmail,
            match["message_id"],
        )

        results.append(
            SemanticSearchResult(
                message_id=match["message_id"],
                score=match["score"],
                subject=message["subject"],
                sender=message["from"],
                snippet=message["snippet"],
            )
        )

    return SemanticSearchResponse(
        results=results,
    )