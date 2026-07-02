import json

from app.ai import ai_client
from app.ai.prompts import (
    INTENT_DETECTION_PROMPT
)
from app.ai.schemas import IntentResult
from app.ai.utils import clean_email_body


class IntentDetector:

    def detect(
        self,
        email_body: str
    ) -> IntentResult:
        cleaned_email_body = clean_email_body(
            email_body
        )

        prompt = (
            INTENT_DETECTION_PROMPT.format(
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

            return IntentResult(
                **parsed_response
            )

        except Exception:
            return IntentResult(
                category="other",
                reason="Unable to determine intent."
            )
