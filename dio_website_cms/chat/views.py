from typing import ClassVar

import requests
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ChatMessageSerializer
from .storage import get_history_chat, save_messages


def get_response(payload: dict) -> dict:
    response = requests.post(
        url=f"/api/v1/chat/{payload['id']}/completion", json=payload, timeout=5
    )

    result = response.json()
    if response.status_code != 200:
        raise Exception(f"API returned status {response.status_code}: {response.text}")
    return result


def get_content(request) -> list | dict:
    serializer = ChatMessageSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {"error": "Invalid input", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    session_id = request.COOKIES.get("sessionid")
    content = serializer.validated_data["content"]
    payload = {"id": session_id, "role": "human", "content": content}

    api_response = get_response(payload)
    save_messages([payload, api_response], session_id)

    return get_history_chat(session_id)


class ChatView(APIView):
    permission_classes: ClassVar[list] = [IsAuthenticated]

    def post(self, request) -> Response:  # noqa: PLR6301
        serializer = ChatMessageSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"error": "Invalid input", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session_id = request.COOKIES.get("sessionid")
        content = serializer.validated_data["content"]
        payload = {"id": session_id, "role": "human", "content": content}

        api_response = get_response(payload)
        save_messages([payload, api_response], session_id)

        return Response(get_history_chat(session_id), status=status.HTTP_200_OK)
