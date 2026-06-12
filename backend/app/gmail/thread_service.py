from app.gmail.message_service import (
    get_header
)

from app.gmail.email_parser import (
    extract_text
)


def get_thread_by_id(
    gmail,
    thread_id: str
):

    thread = (
        gmail.users()
        .threads()
        .get(
            userId="me",
            id=thread_id
        )
        .execute()
    )

    messages = []

    for message in thread.get(
        "messages",
        []
    ):

        payload = message.get(
            "payload",
            {}
        )

        headers = payload.get(
            "headers",
            []
        )

        messages.append(
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
                "to": get_header(
                    headers,
                    "To"
                ),
                "date": get_header(
                    headers,
                    "Date"
                ),
                "snippet": message.get(
                    "snippet",
                    ""
                ),
                "body": extract_text(
                    payload
                ),
                "labelIds": message.get(
                    "labelIds",
                    []
                )
            }
        )

    return {
        "id": thread["id"],
        "historyId": thread.get(
            "historyId"
        ),
        "messageCount": len(
            messages
        ),
        "messages": messages
    }

def get_recent_threads(
    gmail,
    max_results: int = 20
):

    response = (
        gmail.users()
        .threads()
        .list(
            userId="me",
            maxResults=max_results
        )
        .execute()
    )

    threads = response.get(
        "threads",
        []
    )

    result = []

    for thread in threads:

        thread_data = (
            gmail.users()
            .threads()
            .get(
                userId="me",
                id=thread["id"]
            )
            .execute()
        )

        latest_message = (
            thread_data["messages"][-1]
        )

        payload = latest_message.get(
            "payload",
            {}
        )

        headers = payload.get(
            "headers",
            []
        )

        result.append(
            {
                "threadId": thread_data["id"],
                "messageCount": len(
                    thread_data.get(
                        "messages",
                        []
                    )
                ),
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
                "snippet": latest_message.get(
                    "snippet",
                    ""
                )
            }
        )

    return result