from pydantic import BaseModel


class ReplyRequest(
    BaseModel
):
    body: str