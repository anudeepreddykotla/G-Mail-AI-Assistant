from pydantic import BaseModel, Field


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

class EmbeddingResponse(BaseModel):
    success: bool
    message_id: str
    dimensions: int


class SemanticSearchRequest(BaseModel):
    query: str
    limit: int = Field(default=5, ge=1, le=20)


class SemanticSearchResult(BaseModel):
    message_id: str
    score: float
    subject: str
    sender: str
    snippet: str


class SemanticSearchResponse(BaseModel):
    results: list[SemanticSearchResult]


class BulkIndexRequest(BaseModel):
    max_messages: int = Field(default=100, ge=1, le=500)


class BulkIndexResponse(BaseModel):
    processed: int
    indexed: int
    skipped: int
    failed: int