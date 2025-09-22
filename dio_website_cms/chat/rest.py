import requests
from django.core.files.uploadedfile import UploadedFile

from .constants import STATUS_CREATED, STATUS_DELETED, STATUS_OK


def get_ai_response(payload: dict) -> dict:
    response = requests.post(  # noqa: S113
        url=f"http://127.0.0.1:8000/api/v1/chat/{payload['id']}/completion",
        json=payload,
    )
    if response.status_code != STATUS_OK:
        raise Exception(f"API returned status {response.status_code}: {response.text}")  # noqa: TRY002
    return response.json()


def add_document(text: str) -> list:
    response = requests.post(  # noqa: S113
        url="http://127.0.0.1:8000/api/v1/admin/documents",
        json={"text": text},
    )
    if response.status_code != STATUS_CREATED:
        raise Exception(f"API returned status {response.status_code}: {response.text}")  # noqa: TRY002
    return response.json()


def upload_document(file: UploadedFile) -> list:
    response = requests.post(  # noqa: S113
        url="http://127.0.0.1:8000/api/v1/admin/documents/upload",
        files={"file": file},
    )
    if response.status_code != STATUS_CREATED:
        raise Exception(f"API returned status {response.status_code}: {response.text}")  # noqa: TRY002
    return response.json()


def delete_document(ids: list[str]) -> None:
    response = requests.delete(  # noqa: S113
        url="http://127.0.0.1:8000/api/v1/admin/documents",
        json={"ids": ids},
    )
    if response.status_code != STATUS_DELETED:
        raise Exception(f"API returned status {response.status_code}: {response.text}")  # noqa: TRY002
