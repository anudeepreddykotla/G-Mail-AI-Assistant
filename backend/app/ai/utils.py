import re


def clean_email_body(
    email_body: str
) -> str:
    email_body = re.sub(
        r'\n\s*\n',
        '\n',
        email_body
    )

    unsubscribe_patterns = [
        r'Unsubscribe.*',
        r'View in browser.*',
        r'Privacy Policy.*'
    ]

    for pattern in unsubscribe_patterns:
        email_body = re.sub(
            pattern,
            '',
            email_body,
            flags=re.IGNORECASE
        )

    email_body = email_body.strip()

    return email_body