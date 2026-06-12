from fastapi import APIRouter, Depends

from app.auth.current_gmail import get_current_gmail
from app.ai.resolver import AIContentResolver
from app.ai.summarizer import EmailSummarizer
from app.ai.schemas import SummaryResponse, SmartReplyResponse, ActionExtractionResponse, PriorityResponse

from app.db.session import get_db
from sqlalchemy.orm import Session
from app.ai.cache_service import SummaryCacheService
from app.ai.smart_reply import SmartReplyGenerator
from app.ai.extractor import ActionExtractor
from app.ai.classifier import PriorityClassifier

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)

summarizer = EmailSummarizer()

smart_reply_generator = SmartReplyGenerator()

action_extractor = ActionExtractor()

priority_classifier = PriorityClassifier()

@router.post(
    "/messages/{message_id}/summarize",
    response_model=SummaryResponse
)
def summarize_message(
    message_id: str,
    gmail=Depends(
        get_current_gmail
    ),
    db: Session = Depends(
        get_db
    )
):
    cached_summary = (
        SummaryCacheService.get_cached_summary(
            db,
            message_id
        )
    )

    if cached_summary:
        return SummaryResponse(
            message_id=message_id,
            summary=cached_summary
        )

    email_body = (
        AIContentResolver.resolve_message(
            gmail,
            message_id
        )
    )

    summary = summarizer.summarize(
        email_body
    )

    SummaryCacheService.save_summary(
        db,
        message_id,
        summary
    )

    return SummaryResponse(
        message_id=message_id,
        summary=summary
    )

@router.post(
    "/messages/{message_id}/reply",
    response_model=SmartReplyResponse
)
def generate_reply(
    message_id: str,
    gmail=Depends(
        get_current_gmail
    )
):
    email_body = (
        AIContentResolver.resolve_message(
            gmail,
            message_id
        )
    )

    replies = (
        smart_reply_generator.generate(
            email_body
        )
    )

    return SmartReplyResponse(
        message_id=message_id,
        replies=replies
    )

@router.post(
    "/messages/{message_id}/extract",
    response_model=ActionExtractionResponse
)
def extract_actions(
    message_id: str,
    gmail=Depends(
        get_current_gmail
    )
):
    email_body = (
        AIContentResolver.resolve_message(
            gmail,
            message_id
        )
    )

    actions = (
        action_extractor.extract(
            email_body
        )
    )

    return ActionExtractionResponse(
        message_id=message_id,
        actions=actions
    )

@router.post(
    "/messages/{message_id}/classify",
    response_model=PriorityResponse
)
def classify_message_priority(
    message_id: str,
    gmail=Depends(
        get_current_gmail
    )
):
    email_body = (
        AIContentResolver.resolve_message(
            gmail,
            message_id
        )
    )

    priority = (
        priority_classifier.classify(
            email_body
        )
    )

    return PriorityResponse(
        message_id=message_id,
        priority=priority
    )