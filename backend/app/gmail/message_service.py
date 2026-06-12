from concurrent.futures import ThreadPoolExecutor

from app.gmail.email_parser import (
    extract_text,
    extract_html
)


def get_header(
    headers,
    header_name: str
):
    for header in headers:
        if (
            header["name"].lower()
            ==
            header_name.lower()
        ):
            return header["value"]

    return ""


def get_raw_message(
    gmail,
    message_id: str,
    format_type: str = "full",
    metadata_headers: list[str] | None = None
):
    request_args = {
        "userId": "me",
        "id": message_id,
        "format": format_type
    }

    if metadata_headers:
        request_args[
            "metadataHeaders"
        ] = metadata_headers

    return (
        gmail.users()
        .messages()
        .get(
            **request_args
        )
        .execute()
    )


def get_recent_messages(
    gmail,
    max_results: int = 20,
    label_ids: list[str] | None = None,
    include_spam_trash: bool = False,
    page_token: str | None = None
):
    request_args = {
        "userId": "me",
        "maxResults": max_results,
    }

    if label_ids:
        request_args["labelIds"] = label_ids

    if include_spam_trash:
        request_args["includeSpamTrash"] = True

    if page_token:
        request_args["pageToken"] = page_token

    response = (
        gmail.users()
        .messages()
        .list(**request_args)
        .execute()
    )

    messages = response.get(
        "messages",
        []
    )

    result = []

    for msg in messages:
        message = (
            gmail.users()
            .messages()
            .get(
                userId="me",
                id=msg["id"],
                format="metadata",
                metadataHeaders=[
                    "Subject",
                    "From",
                    "Date"
                ]
            )
            .execute()
        )

        headers = (
            message
            .get("payload", {})
            .get("headers", [])
        )

        result.append(
            {
                "id": message["id"],
                "threadId": message["threadId"],
                "subject": get_header(
                    headers,
                    "Subject"
                ),
                "from": get_header(
                    headers,
                    "From"
                ),
                "date": get_header(
                    headers,
                    "Date"
                ),
                "snippet": message.get(
                    "snippet",
                    ""
                ),
                "labelIds": message.get(
                    "labelIds",
                    []
                )
            }
        )

    return {
        "messages": result,
        "nextPageToken": response.get(
            "nextPageToken"
        )
    }


def get_message_by_id(
    gmail,
    message_id: str
):
    message = get_raw_message(
        gmail,
        message_id,
        format_type="full"
    )

    payload = message.get(
        "payload",
        {}
    )

    headers = payload.get(
        "headers",
        []
    )

    subject = get_header(
        headers,
        "Subject"
    )

    sender = get_header(
        headers,
        "From"
    )

    receiver = get_header(
        headers,
        "To"
    )

    date = get_header(
        headers,
        "Date"
    )

    body = extract_text(
        payload
    )

    html_body = extract_html(
        payload
    )

    return {
        "id": message["id"],
        "threadId": message["threadId"],
        "subject": subject,
        "from": sender,
        "to": receiver,
        "date": date,
        "snippet": message.get(
            "snippet",
            ""
        ),
        "body": body,
        "htmlBody": html_body,
        "labelIds": message.get(
            "labelIds",
            []
        )
    }