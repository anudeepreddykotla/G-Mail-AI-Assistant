import base64

from email.mime.text import MIMEText

import base64

from email.mime.text import MIMEText
from email.utils import parseaddr

from app.gmail.message_service import (
    get_raw_message,
    get_header
)

def build_message(
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

    return message


def encode_message(
    message
):

    return (
        base64.urlsafe_b64encode(
            message.as_bytes()
        )
        .decode()
    )


def send_email(
    gmail,
    to: str,
    subject: str,
    body: str
):

    message = build_message(
        to,
        subject,
        body
    )

    raw_message = encode_message(
        message
    )

    sent_message = (
        gmail.users()
        .messages()
        .send(
            userId="me",
            body={
                "raw": raw_message
            }
        )
        .execute()
    )

    return {
        "id": sent_message["id"],
        "threadId": sent_message["threadId"]
    }

def build_reply_message(
    to: str,
    subject: str,
    body: str,
    message_id: str,
    references: str = ""
):

    message = MIMEText(
        body,
        "plain",
        "utf-8"
    )

    message["To"] = to

    if subject.startswith("Re:"):

        message["Subject"] = subject

    else:

        message["Subject"] = f"Re: {subject}"

    message["In-Reply-To"] = message_id

    if references:

        message["References"] = (
            references
            + " "
            + message_id
        )

    else:

        message["References"] = message_id

    return message

def get_reply_metadata(
    gmail,
    original_message_id: str
):

    original = get_raw_message(
        gmail,
        original_message_id
    )

    payload = original.get(
        "payload",
        {}
    )

    headers = payload.get(
        "headers",
        []
    )

    sender = parseaddr(
        get_header(
            headers,
            "From"
        )
    )[1]

    subject = get_header(
        headers,
        "Subject"
    )

    message_id = get_header(
        headers,
        "Message-ID"
    )

    references = get_header(
        headers,
        "References"
    )

    return {
        "to": sender,
        "subject": subject,
        "message_id": message_id,
        "references": references,
        "thread_id": original[
            "threadId"
        ]
    }

def reply_email(
    gmail,
    original_message_id: str,
    body: str
):

    metadata = get_reply_metadata(
        gmail,
        original_message_id
    )

    message = build_reply_message(
        to=metadata["to"],
        subject=metadata["subject"],
        body=body,
        message_id=metadata["message_id"],
        references=metadata["references"]
    )

    raw_message = encode_message(
        message
    )

    sent_message = (
        gmail.users()
        .messages()
        .send(
            userId="me",
            body={
                "raw": raw_message,
                "threadId": metadata[
                    "thread_id"
                ]
            }
        )
        .execute()
    )

    return {
        "id": sent_message["id"],
        "threadId": sent_message["threadId"]
    }