from pydantic import BaseModel


class EmailSummary(BaseModel):
    short_summary: str
    bullet_points: list[str]
    action_items: list[str]

class SummaryResponse(BaseModel):
    message_id: str
    summary: EmailSummary

class SmartReplyOptions(BaseModel):
    formal: str
    casual: str
    concise: str


class SmartReplyResponse(BaseModel):
    message_id: str
    replies: SmartReplyOptions

class ExtractedTask(BaseModel):
    task: str
    deadline: str | None = None


class ActionExtractionResult(BaseModel):
    tasks: list[ExtractedTask]


class ActionExtractionResponse(BaseModel):
    message_id: str
    actions: ActionExtractionResult

class PriorityResult(BaseModel):
    level: str
    reason: str


class PriorityResponse(BaseModel):
    message_id: str
    priority: PriorityResult

class IntentResult(BaseModel):
    category: str
    reason: str


class IntentResponse(BaseModel):
    message_id: str
    intent: IntentResult

class LabelSuggestionResult(BaseModel):
    labels: list[str]


class LabelSuggestionResponse(BaseModel):
    message_id: str
    suggestions: LabelSuggestionResult

class ReminderItem(BaseModel):
    title: str
    datetime: str | None = None
    priority: str


class ReminderExtractionResult(BaseModel):
    reminders: list[ReminderItem]


class ReminderResponse(BaseModel):
    message_id: str
    reminders: ReminderExtractionResult