from pydantic import BaseModel


class SendEmailRequest(
    BaseModel
):
    to: str

    subject: str

    body: str

    thread_id: str | None = None

    in_reply_to: str | None = None

    references: str | None = None