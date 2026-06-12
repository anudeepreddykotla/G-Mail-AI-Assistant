import base64
import re
from html import unescape

from bs4 import BeautifulSoup


def decode_body(data: str) -> str:

    try:

        decoded = base64.urlsafe_b64decode(
            data
        )

        return decoded.decode(
            "utf-8",
            errors="ignore"
        )

    except Exception:

        return ""


def html_to_text(html: str) -> str:

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    for tag in soup(
        [
            "script",
            "style",
            "head",
            "title",
            "meta"
        ]
    ):

        tag.decompose()

    text = soup.get_text(
        separator="\n"
    )

    text = unescape(
        text
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


def clean_text(text: str) -> str:

    text = re.sub(
        r"[\u034f\u2007\u200b-\u200f\u202a-\u202e\u2060\ufeff]",
        "",
        text
    )

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    text = re.sub(
        r"(?im)^unsubscribe.*$",
        "",
        text
    )

    text = re.sub(
        r"\n{2,}",
        "\n\n",
        text
    )

    return text.strip()


def extract_text(payload):

    if payload is None:
        return ""

    mime_type = payload.get(
        "mimeType",
        ""
    )

    body = payload.get(
        "body",
        {}
    )

    data = body.get(
        "data"
    )

    if data:

        decoded = decode_body(
            data
        )

        if mime_type == "text/plain":

            return clean_text(
                decoded
            )

        if mime_type == "text/html":

            return clean_text(
                html_to_text(
                    decoded
                )
            )

    parts = payload.get(
        "parts",
        []
    )

    for part in parts:

        text = extract_text(
            part
        )

        if text:

            return text

    return ""

def extract_html(payload):

    if payload is None:
        return ""

    mime_type = payload.get(
        "mimeType",
        ""
    )

    body = payload.get(
        "body",
        {}
    )

    data = body.get(
        "data"
    )

    if data and mime_type == "text/html":

        return decode_body(
            data
        )

    parts = payload.get(
        "parts",
        []
    )

    for part in parts:

        html = extract_html(
            part
        )

        if html:

            return html

    return ""