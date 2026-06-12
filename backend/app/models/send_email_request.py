from pydantic import BaseModel


class SendEmailRequest(BaseModel):

    to: str

    subject: str

    body: str