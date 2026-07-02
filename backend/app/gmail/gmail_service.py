from googleapiclient.discovery import build
from google_auth_httplib2 import AuthorizedHttp
import httplib2


def get_gmail_service(credentials):
    http = httplib2.Http(timeout=60)

    authed_http = AuthorizedHttp(
        credentials,
        http=http
    )

    return build(
        "gmail",
        "v1",
        http=authed_http
    )