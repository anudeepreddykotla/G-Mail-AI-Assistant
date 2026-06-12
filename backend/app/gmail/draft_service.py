import base64

from email.mime.text import MIMEText

from app.gmail.message_service import (
    get_header
)

from app.gmail.email_parser import (
    extract_text
)

def create_draft(
    gmail,
    to: str,
    subject: str,
    body: str
):

    message = MIMEText(
        body,
        "plain",
        "utf-8"
    )

    message["To"] = to
    message["Subject"] = subject

    raw_message = (
        base64.urlsafe_b64encode(
            message.as_bytes()
        )
        .decode()
    )

    draft = (
        gmail.users()
        .drafts()
        .create(
            userId="me",
            body={
                "message": {
                    "raw": raw_message
                }
            }
        )
        .execute()
    )

    return {
        "id": draft["id"],
        "messageId": draft["message"]["id"]
    }

def list_drafts(
    gmail,
    max_results: int = 20
):

    response = (
        gmail.users()
        .drafts()
        .list(
            userId="me",
            maxResults=max_results
        )
        .execute()
    )

    drafts = response.get(
        "drafts",
        []
    )

    result = []

    for draft in drafts:

        draft_data = (
            gmail.users()
            .drafts()
            .get(
                userId="me",
                id=draft["id"]
            )
            .execute()
        )

        message = draft_data[
            "message"
        ]

        payload = message.get(
            "payload",
            {}
        )

        headers = payload.get(
            "headers",
            []
        )

        result.append(
            {
                "id": draft_data["id"],
                "messageId": message["id"],
                "threadId": message.get(
                    "threadId"
                ),
                "subject": get_header(
                    headers,
                    "Subject"
                ),
                "to": get_header(
                    headers,
                    "To"
                ),
                "snippet": message.get(
                    "snippet",
                    ""
                ),
                "body": extract_text(
                    payload
                )
            }
        )

    return result

def get_draft(
    gmail,
    draft_id: str
):

    draft = (
        gmail.users()
        .drafts()
        .get(
            userId="me",
            id=draft_id
        )
        .execute()
    )

    message = draft[
        "message"
    ]

    payload = message.get(
        "payload",
        {}
    )

    headers = payload.get(
        "headers",
        []
    )

    return {
        "id": draft["id"],
        "messageId": message["id"],
        "threadId": message.get(
            "threadId"
        ),
        "subject": get_header(
            headers,
            "Subject"
        ),
        "to": get_header(
            headers,
            "To"
        ),
        "snippet": message.get(
            "snippet",
            ""
        ),
        "body": extract_text(
            payload
        )
    }

def delete_draft(
    gmail,
    draft_id: str
):

    (
        gmail.users()
        .drafts()
        .delete(
            userId="me",
            id=draft_id
        )
        .execute()
    )

    return {
        "id": draft_id,
        "status": "deleted"
    }