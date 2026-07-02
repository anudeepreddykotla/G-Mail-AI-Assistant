import json

from app.ai import ai_client
from app.ai.prompts import (
    REMINDER_EXTRACTION_PROMPT
)
from app.ai.schemas import (
    ReminderExtractionResult
)
from app.ai.utils import clean_email_body


class ReminderExtractor:

    def extract(
        self,
        email_body: str
    ) -> ReminderExtractionResult:
        cleaned_email_body = clean_email_body(
            email_body
        )

        prompt = (
            REMINDER_EXTRACTION_PROMPT.format(
                email_body=cleaned_email_body
            )
        )

        response = ai_client.generate(
            prompt
        )

        try:
            cleaned_response = (
                response
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            parsed_response = json.loads(
                cleaned_response
            )

            return ReminderExtractionResult(
                **parsed_response
            )

        except Exception:
            return ReminderExtractionResult(
                reminders=[]
            )
