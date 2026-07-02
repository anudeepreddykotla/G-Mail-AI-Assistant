from app.ai.schemas import (
    LabelSuggestionResult
)


INTENT_LABEL_MAP = {
    "job_opportunity": [
        "Career",
        "Jobs"
    ],
    "internship": [
        "Career",
        "Internship"
    ],
    "interview": [
        "Career",
        "Interview",
        "Important"
    ],
    "hackathon": [
        "Career",
        "Hackathon"
    ],
    "contest": [
        "Career",
        "Contest"
    ],
    "meeting": [
        "Meetings",
        "Important"
    ],
    "project_update": [
        "Work",
        "Project"
    ],
    "payment_due": [
        "Finance",
        "Urgent"
    ],
    "invoice": [
        "Finance"
    ],
    "academic": [
        "College",
        "Academic"
    ],
    "otp": [
        "Security"
    ],
    "promotion": [
        "Promotions"
    ],
    "newsletter": [
        "Updates"
    ],
    "personal": [
        "Personal"
    ],
    "other": [
        "General"
    ]
}


class LabelSuggester:

    def suggest(
        self,
        intent_category: str
    ) -> LabelSuggestionResult:
        labels = INTENT_LABEL_MAP.get(
            intent_category,
            ["General"]
        )

        return LabelSuggestionResult(
            labels=labels
        )
