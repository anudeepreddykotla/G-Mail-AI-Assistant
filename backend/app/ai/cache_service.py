import json

from sqlalchemy.orm import Session

from app.models.email_summary import (
    EmailSummaryCache
)
from app.ai.schemas import (
    EmailSummary
)


class SummaryCacheService:

    @staticmethod
    def get_cached_summary(
        db: Session,
        message_id: str
    ) -> EmailSummary | None:
        cached_summary = (
            db.query(
                EmailSummaryCache
            )
            .filter(
                EmailSummaryCache.message_id
                ==
                message_id
            )
            .first()
        )

        if cached_summary:
            print("CACHE HIT")

        if not cached_summary:
            return None

        return EmailSummary(
            short_summary=(
                cached_summary.short_summary
            ),
            bullet_points=json.loads(
                cached_summary.bullet_points
            ),
            action_items=json.loads(
                cached_summary.action_items
            )
        )

    @staticmethod
    def save_summary(
        db: Session,
        message_id: str,
        summary: EmailSummary
    ):
        cache_entry = EmailSummaryCache(
            message_id=message_id,
            short_summary=(
                summary.short_summary
            ),
            bullet_points=json.dumps(
                summary.bullet_points
            ),
            action_items=json.dumps(
                summary.action_items
            )
        )

        db.add(cache_entry)
        db.commit()