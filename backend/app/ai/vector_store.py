from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models.email_embedding import EmailEmbedding


def save_embedding(
    db: Session,
    message_id: str,
    embedding: list[float],
    model: str,
):
    existing = (
        db.query(EmailEmbedding)
        .filter_by(message_id=message_id)
        .first()
    )

    if existing:
        existing.embedding = embedding
        existing.model = model
    else:
        db.add(
            EmailEmbedding(
                message_id=message_id,
                embedding=embedding,
                model=model,
            )
        )

    db.commit()


def get_embedding(
    db: Session,
    message_id: str,
):
    return (
        db.query(EmailEmbedding)
        .filter_by(message_id=message_id)
        .first()
    )


def search_similar(
    db: Session,
    embedding: list[float],
    limit: int = 5,
):
    sql = text("""
        SELECT
            message_id,
            1 - (embedding <=> CAST(:embedding AS vector)) AS score
        FROM email_embeddings
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT :limit
    """)

    result = db.execute(
        sql,
        {
            "embedding": str(embedding),
            "limit": limit,
        },
    )

    return [
        {
            "message_id": row.message_id,
            "score": float(row.score),
        }
        for row in result
    ]