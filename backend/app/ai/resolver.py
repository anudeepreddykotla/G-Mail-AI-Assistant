from app.gmail.message_service import (
    get_message_by_id
)

from app.gmail.thread_service import (
    get_thread_by_id
)


class AIContentResolver:

    @staticmethod
    def resolve_message(
        gmail,
        message_id: str
    ) -> str:
        message = get_message_by_id(
            gmail,
            message_id
        )

        return message["body"]

    @staticmethod
    def resolve_thread(
        gmail,
        thread_id: str
    ) -> str:
        thread = get_thread_by_id(
            gmail,
            thread_id
        )

        combined_messages = []

        for message in thread["messages"]:
            combined_messages.append(
                f"""
From: {message["from"]}
Date: {message["date"]}

{message["body"]}
"""
            )

        return "\n\n---\n\n".join(
            combined_messages
        )