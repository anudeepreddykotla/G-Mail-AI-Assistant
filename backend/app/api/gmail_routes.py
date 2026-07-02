from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
import time

from app.gmail.message_service import (
    get_recent_messages,
    get_message_by_id
)

from app.gmail.message_actions import (
    mark_as_read,
    mark_as_unread,
    archive_message,
    unarchive_message,
    trash_message as move_to_trash,
    restore_message as restore_from_trash,
    star_message,
    unstar_message
)

from app.gmail.send_service import (
    send_email,
    reply_email
)

from app.models.send_email_request import (
    SendEmailRequest
)

from app.models.reply_request import (
    ReplyRequest
)

from app.gmail.search_service import (
    search_messages
)

from app.gmail.thread_service import (
    get_recent_threads,
    get_thread_by_id
)

from app.gmail.draft_service import (
    create_draft,
    list_drafts,
    get_draft,
    update_draft,
    send_draft,
    delete_draft
)

from app.gmail.label_service import (
    list_labels,
    create_label,
    apply_label,
    remove_label
)

from app.models.label_action_request import (
    LabelActionRequest
)

from app.models.create_label_request import (
    CreateLabelRequest
)

from app.auth.current_gmail import (
    get_current_gmail
)

router = APIRouter(
    prefix="/gmail",
    tags=["gmail"]
)


@router.get("/profile")
def gmail_profile(
    gmail=Depends(get_current_gmail)
):
    profile = (
        gmail.users()
        .getProfile(userId="me")
        .execute()
    )

    return profile


@router.get("/messages")
def gmail_messages(
    max_results: int = 20,
    label_id: list[str] | None = Query(
        default=None
    ),
    include_spam_trash: bool = False,
    page_token: str | None = None,
    gmail=Depends(get_current_gmail)
):
    t1 = time.time()
    result = get_recent_messages(
        gmail,
        max_results=max_results,
        label_ids=label_id,
        include_spam_trash=include_spam_trash,
        page_token=page_token
    )
    print("gmail:", time.time()-t1)
    return {
        "count": len(
            result["messages"]
        ),
        "messages": result["messages"],
        "nextPageToken": result.get(
            "nextPageToken"
        )
    }

@router.get("/messages/{message_id}")
def gmail_message(
    message_id: str,
    gmail=Depends(get_current_gmail)
):
    return get_message_by_id(
        gmail,
        message_id
    )


@router.get("/debug/message/{message_id}")
def debug_message(
    message_id: str,
    gmail=Depends(get_current_gmail)
):
    message = (
        gmail.users()
        .messages()
        .get(
            userId="me",
            id=message_id
        )
        .execute()
    )

    return message["payload"]


@router.post("/messages/{message_id}/read")
def read_message(
    message_id: str,
    gmail=Depends(get_current_gmail)
):
    mark_as_read(gmail, message_id)

    return {
        "success": True,
        "message_id": message_id,
        "status": "read"
    }


@router.post("/messages/{message_id}/unread")
def unread_message(
    message_id: str,
    gmail=Depends(get_current_gmail)
):
    mark_as_unread(gmail, message_id)

    return {
        "success": True,
        "message_id": message_id,
        "status": "unread"
    }


@router.post("/send")
def gmail_send(
    request: SendEmailRequest,
    gmail=Depends(get_current_gmail)
):
    return send_email(
        gmail=gmail,
        to=request.to,
        subject=request.subject,
        body=request.body
    )


@router.post("/messages/{message_id}/trash")
def trash_message_route(
    message_id: str,
    gmail=Depends(get_current_gmail)
):
    return move_to_trash(gmail, message_id)


@router.post("/messages/{message_id}/restore")
def restore_message_route(
    message_id: str,
    gmail=Depends(get_current_gmail)
):
    return restore_from_trash(gmail, message_id)


@router.post("/messages/{message_id}/archive")
def archive(
    message_id: str,
    gmail=Depends(get_current_gmail)
):
    return archive_message(gmail, message_id)

@router.post(
    "/messages/{message_id}/unarchive"
)
def unarchive(
    message_id: str,
    gmail=Depends(get_current_gmail)
):
    return unarchive_message(
        gmail,
        message_id
    )


@router.post("/messages/{message_id}/star")
def star(
    message_id: str,
    gmail=Depends(get_current_gmail)
):
    return star_message(gmail, message_id)


@router.post("/messages/{message_id}/unstar")
def unstar(
    message_id: str,
    gmail=Depends(get_current_gmail)
):
    return unstar_message(gmail, message_id)


@router.get("/search")
def gmail_search(
    q: str = Query(...),
    max_results: int = 20,
    gmail=Depends(get_current_gmail)
):
    messages = search_messages(
        gmail,
        query=q,
        max_results=max_results
    )

    return {
        "query": q,
        "count": len(messages),
        "messages": messages
    }


@router.post("/messages/{message_id}/reply")
def reply_to_message(
    message_id: str,
    request: ReplyRequest,
    gmail=Depends(get_current_gmail)
):
    return reply_email(
        gmail,
        message_id,
        request.body
    )


@router.get("/threads")
def gmail_threads(
    gmail=Depends(get_current_gmail)
):
    threads = get_recent_threads(
        gmail,
        max_results=20
    )

    return {
        "count": len(threads),
        "threads": threads
    }


@router.get("/threads/{thread_id}")
def gmail_thread(
    thread_id: str,
    gmail=Depends(get_current_gmail)
):
    return get_thread_by_id(gmail, thread_id)


@router.post("/drafts")
def create_email_draft(
    request: SendEmailRequest,
    gmail=Depends(get_current_gmail)
):
    return create_draft(
        gmail,
        request.to,
        request.subject,
        request.body,
        request.thread_id,
        request.in_reply_to,
        request.references
    )


@router.get("/drafts")
def gmail_drafts(
    gmail=Depends(get_current_gmail)
):
    drafts = list_drafts(gmail)

    return {
        "count": len(drafts),
        "drafts": drafts
    }


@router.get("/drafts/{draft_id}")
def gmail_draft(
    draft_id: str,
    gmail=Depends(get_current_gmail)
):
    return get_draft(gmail, draft_id)

@router.put("/drafts/{draft_id}")
def edit_draft(
    draft_id: str,
    request: SendEmailRequest,
    gmail=Depends(get_current_gmail)
):
    return update_draft(
        gmail,
        draft_id,
        request.to,
        request.subject,
        request.body,
        request.thread_id,
        request.in_reply_to,
        request.references
    )

@router.post("/drafts/{draft_id}/send")
def send_email_draft(
    draft_id: str,
    gmail=Depends(get_current_gmail)
):
    return send_draft(
        gmail,
        draft_id
    )

@router.delete("/drafts/{draft_id}")
def remove_draft(
    draft_id: str,
    gmail=Depends(get_current_gmail)
):
    return delete_draft(gmail, draft_id)


@router.get("/labels")
def gmail_labels(
    gmail=Depends(get_current_gmail)
):
    labels = list_labels(gmail)

    return {
        "count": len(labels),
        "labels": labels
    }


@router.post("/labels")
def gmail_create_label(
    request: CreateLabelRequest,
    gmail=Depends(get_current_gmail)
):
    return create_label(gmail, request.name)


@router.post("/messages/{message_id}/labels/apply")
def apply_message_label(
    message_id: str,
    request: LabelActionRequest,
    gmail=Depends(get_current_gmail)
):
    return apply_label(
        gmail,
        message_id,
        request.label_id
    )


@router.post("/messages/{message_id}/labels/remove")
def remove_message_label(
    message_id: str,
    request: LabelActionRequest,
    gmail=Depends(get_current_gmail)
):
    return remove_label(
        gmail,
        message_id,
        request.label_id
    )