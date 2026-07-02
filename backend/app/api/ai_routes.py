from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from app.auth.current_gmail import get_current_gmail

from app.db.session import get_db

from app.gmail.message_service import (
    get_message_by_id
)

from app.ai.label_suggester import (
    LabelSuggester
)

from app.ai.intent_detector import (
    IntentDetector
)

from app.ai.reminder_extractor import (
    ReminderExtractor
)

from app.ai.resolver import AIContentResolver
from app.ai.summarizer import EmailSummarizer
from app.ai.smart_reply import SmartReplyGenerator
from app.ai.extractor import ActionExtractor
from app.ai.classifier import PriorityClassifier
from app.ai.cache_service import SummaryCacheService

from app.ai.schemas import (
    SummaryResponse,
    SmartReplyResponse,
    ActionExtractionResponse,
    PriorityResponse,
    IntentResponse,
    LabelSuggestionResponse,
    ReminderResponse
)

from app.gmail.thread_service import (
    get_thread_by_id
)


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


summarizer = EmailSummarizer()

smart_reply_generator = (
    SmartReplyGenerator()
)

action_extractor = (
    ActionExtractor()
)

priority_classifier = (
    PriorityClassifier()
)

intent_detector = (
    IntentDetector()
)

label_suggester = (
    LabelSuggester()
)

reminder_extractor = (
    ReminderExtractor()
)


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
    message = get_message_by_id(
        gmail,
        message_id
    )

    replies = (
        smart_reply_generator.generate(
            message["body"],
            message["from"]
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

@router.post(
    "/threads/{thread_id}/summarize",
    response_model=SummaryResponse
)
def summarize_thread(
    thread_id: str,
    gmail=Depends(
        get_current_gmail
    )
):
    thread_content = (
        AIContentResolver.resolve_thread(
            gmail,
            thread_id
        )
    )

    summary = summarizer.summarize(
        thread_content
    )

    return SummaryResponse(
        message_id=thread_id,
        summary=summary
    )

@router.post(
    "/threads/{thread_id}/reply",
    response_model=SmartReplyResponse
)
def generate_thread_reply(
    thread_id: str,
    gmail=Depends(
        get_current_gmail
    )
):
    profile = (
        gmail.users()
        .getProfile(
            userId="me"
        )
        .execute()
    )

    my_email = profile[
        "emailAddress"
    ].lower()

    thread = get_thread_by_id(
        gmail,
        thread_id
    )

    thread_content = (
        AIContentResolver.resolve_thread(
            gmail,
            thread_id
        )
    )

    reply_target = None

    for message in reversed(
        thread["messages"]
    ):
        sender = (
            message["from"]
            .lower()
        )

        if my_email not in sender:
            reply_target = (
                message["from"]
            )
            break

    replies = (
        smart_reply_generator.generate(
            thread_content,
            reply_target or ""
        )
    )

    return SmartReplyResponse(
        message_id=thread_id,
        replies=replies
    )

@router.post(
    "/messages/{message_id}/intent",
    response_model=IntentResponse
)
def detect_message_intent(
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

    intent = (
        intent_detector.detect(
            email_body
        )
    )

    return IntentResponse(
        message_id=message_id,
        intent=intent
    )

@router.post(
    "/messages/{message_id}/labels",
    response_model=LabelSuggestionResponse
)
def suggest_labels(
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

    intent = (
        intent_detector.detect(
            email_body
        )
    )

    suggestions = (
        label_suggester.suggest(
            intent.category
        )
    )

    return LabelSuggestionResponse(
        message_id=message_id,
        suggestions=suggestions
    )

@router.post(
    "/messages/{message_id}/reminders",
    response_model=ReminderResponse
)
def extract_reminders(
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

    reminders = (
        reminder_extractor.extract(
            email_body
        )
    )

    return ReminderResponse(
        message_id=message_id,
        reminders=reminders
    )