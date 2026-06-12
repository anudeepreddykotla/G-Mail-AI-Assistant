import json

from app.ai import ai_client
from app.ai.prompts import SUMMARY_PROMPT
from app.ai.schemas import EmailSummary
from app.ai.utils import clean_email_body


import json


class EmailSummarizer:

    def summarize(
        self,
        email_body: str
    ) -> EmailSummary:
        cleaned_email_body = clean_email_body(
            email_body
        )

        prompt = SUMMARY_PROMPT.format(
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

            return EmailSummary(
                **parsed_response
            )

        except Exception as e:
            print("SUMMARY ERROR:", e)
            print("RAW RESPONSE:", response)

            return EmailSummary(
                short_summary="Unable to summarize email.",
                bullet_points=[],
                action_items=[]
            )