import json

from app.ai import ai_client
from app.ai.prompts import SMART_REPLY_PROMPT
from app.ai.schemas import SmartReplyOptions
from app.ai.utils import clean_email_body


class SmartReplyGenerator:

    def generate(
        self,
        email_body: str
    ) -> SmartReplyOptions:
        cleaned_email_body = clean_email_body(
            email_body
        )

        prompt = SMART_REPLY_PROMPT.format(
            email_body=cleaned_email_body
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

            return SmartReplyOptions(
                **parsed_response
            )

        except Exception:
            return SmartReplyOptions(
                formal="Unable to generate reply.",
                casual="Unable to generate reply.",
                concise="Unable to generate reply."
            )