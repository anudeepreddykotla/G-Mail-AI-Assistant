from app.gmail.message_service import (
    get_message_by_id
)


def search_messages(
    gmail,
    query: str,
    max_results: int = 20
):

    response = (
        gmail.users()
        .messages()
        .list(
            userId="me",
            q=query,
            maxResults=max_results
        )
        .execute()
    )

    messages = response.get(
        "messages",
        []
    )

    results = []

    for message in messages:

        results.append(
            get_message_by_id(
                gmail,
                message["id"]
            )
        )

    return results