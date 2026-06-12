def mark_as_read(
    gmail,
    message_id: str
):

    return (
        gmail.users()
        .messages()
        .modify(
            userId="me",
            id=message_id,
            body={
                "removeLabelIds": [
                    "UNREAD"
                ]
            }
        )
        .execute()
    )


def mark_as_unread(
    gmail,
    message_id: str
):

    return (
        gmail.users()
        .messages()
        .modify(
            userId="me",
            id=message_id,
            body={
                "addLabelIds": [
                    "UNREAD"
                ]
            }
        )
        .execute()
    )

def star_message(
    gmail,
    message_id: str
):

    return (
        gmail.users()
        .messages()
        .modify(
            userId="me",
            id=message_id,
            body={
                "addLabelIds": [
                    "STARRED"
                ]
            }
        )
        .execute()
    )

def unstar_message(
    gmail,
    message_id: str
):

    return (
        gmail.users()
        .messages()
        .modify(
            userId="me",
            id=message_id,
            body={
                "removeLabelIds": [
                    "STARRED"
                ]
            }
        )
        .execute()
    )

def archive_message(
    gmail,
    message_id: str
):

    return (
        gmail.users()
        .messages()
        .modify(
            userId="me",
            id=message_id,
            body={
                "removeLabelIds": [
                    "INBOX"
                ]
            }
        )
        .execute()
    )


def unarchive_message(
    gmail,
    message_id: str
):
    return (
        gmail.users()
        .messages()
        .modify(
            userId="me",
            id=message_id,
            body={
                "addLabelIds": [
                    "INBOX"
                ]
            }
        )
        .execute()
    )

def trash_message(
    gmail,
    message_id: str
):

    return (
        gmail.users()
        .messages()
        .trash(
            userId="me",
            id=message_id
        )
        .execute()
    )


def restore_message(
    gmail,
    message_id: str
):

    return (
        gmail.users()
        .messages()
        .untrash(
            userId="me",
            id=message_id
        )
        .execute()
    )