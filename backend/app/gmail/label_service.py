def list_labels(
    gmail
):

    response = (
        gmail.users()
        .labels()
        .list(
            userId="me"
        )
        .execute()
    )

    return response.get(
        "labels",
        []
    )

def create_label(
    gmail,
    name: str
):

    label = (
        gmail.users()
        .labels()
        .create(
            userId="me",
            body={
                "name": name,
                "labelListVisibility": "labelShow",
                "messageListVisibility": "show"
            }
        )
        .execute()
    )

    return {
        "id": label["id"],
        "name": label["name"]
    }

def apply_label(
    gmail,
    message_id: str,
    label_id: str
):

    return (
        gmail.users()
        .messages()
        .modify(
            userId="me",
            id=message_id,
            body={
                "addLabelIds": [
                    label_id
                ]
            }
        )
        .execute()
    )

def remove_label(
    gmail,
    message_id: str,
    label_id: str
):

    return (
        gmail.users()
        .messages()
        .modify(
            userId="me",
            id=message_id,
            body={
                "removeLabelIds": [
                    label_id
                ]
            }
        )
        .execute()
    )