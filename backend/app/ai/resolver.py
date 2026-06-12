from app.gmail.message_service import get_message_by_id


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