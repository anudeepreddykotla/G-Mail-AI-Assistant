import json

from app.ai import ai_client
from app.ai.prompts import (
    PRIORITY_CLASSIFICATION_PROMPT
)
from app.ai.schemas import PriorityResult
from app.ai.utils import clean_email_body


class PriorityClassifier:

    def classify(
        self,
        email_body: str
    ) -> PriorityResult:
        cleaned_email_body = clean_email_body(
            email_body
        )

        prompt = (
            PRIORITY_CLASSIFICATION_PROMPT.format(
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

            return PriorityResult(
                **parsed_response
            )

        except Exception:
            return PriorityResult(
                level="low",
                reason="Unable to determine priority."
            )