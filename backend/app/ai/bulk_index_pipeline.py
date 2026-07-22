import time

from google.genai.errors import ClientError
from sqlalchemy.orm import Session

from app.ai.embedding_pipeline import generate_and_store_embedding
from app.ai.schemas import BulkIndexResponse
from app.gmail.message_service import list_message_ids
from app.ai.vector_store import get_embedding


MAX_RETRIES = 3
THROTTLE_SECONDS = 1


def bulk_index(
    db: Session,
    gmail,
    max_messages: int,
) -> BulkIndexResponse:
    messages = list_message_ids(
        gmail,
        max_results=max_messages,
    )

    processed = 0
    indexed = 0
    skipped = 0
    failed = 0

    for message in messages:
        processed += 1

        existing = get_embedding(
            db=db,
            message_id=message["id"],
        )
        if existing:
            skipped += 1
            print(f"Skipping {message['id']} (already indexed)")
            continue

        for attempt in range(MAX_RETRIES):
            try:
                generate_and_store_embedding(
                    db=db,
                    gmail=gmail,
                    message_id=message["id"],
                )

                indexed += 1

                # Throttle Gemini requests
                time.sleep(THROTTLE_SECONDS)
                break

            except ClientError as e:
                status = getattr(e, "status_code", None)

                if status == 429 and attempt < MAX_RETRIES - 1:
                    wait = 2 ** attempt

                    print(
                        f"Rate limited while indexing {message['id']}. "
                        f"Retrying in {wait}s..."
                    )

                    time.sleep(wait)
                    continue

                print(f"Failed to index {message['id']}: {e}")
                failed += 1
                break

            except Exception as e:
                print(f"Failed to index {message['id']}: {e}")
                failed += 1
                break

    return BulkIndexResponse(
        processed=processed,
        indexed=indexed,
        skipped=skipped,
        failed=failed,
    )