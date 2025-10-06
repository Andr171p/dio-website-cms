import requests

from .constants import STATUS_CREATED


def add_document(data: dict) -> list:
    response = requests.post(  # noqa: S113
        url="http://127.0.0.1:8000/api/v1/documents",
        json=data,
    )
    if response.status_code != STATUS_CREATED:
        raise Exception(f"API returned status {response.status_code}: {response.text}")  # noqa: TRY002
    return response.json()


def upload_document(file: bytes) -> list:
    response = requests.post(  # noqa: S113
        url="http://127.0.0.1:8000/api/v1/documents/upload",
        files={"file": file},
    )
    if response.status_code != STATUS_CREATED:
        raise Exception(f"API returned status {response.status_code}: {response.text}")  # noqa: TRY002
    return response.json()
