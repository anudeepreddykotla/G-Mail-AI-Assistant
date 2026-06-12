from pydantic import BaseModel


class CreateLabelRequest(
    BaseModel
):
    name: str