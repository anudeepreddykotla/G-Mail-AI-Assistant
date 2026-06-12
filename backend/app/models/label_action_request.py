from pydantic import BaseModel


class LabelActionRequest(
    BaseModel
):
    label_id: str