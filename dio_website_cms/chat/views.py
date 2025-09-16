from typing import ClassVar

import json

import requests
from django.core.cache import cache
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ChatMessageSerializer


class ChatView(APIView):
    permission_classes: ClassVar[list] = [IsAuthenticated]

    async def post(self, request):
        serializer = ChatMessageSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"error": "Invalid input", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session_id = request.COOKIES.get("sessionid")
        content = serializer.validated_data["content"]
        payload = {"role": "human", "content": content}

        api_response = self.get_response(payload, session_id)
        self.save_message(payload, session_id)
        self.save_message(api_response, api_response["id"])

        return await self.get_history_chat(session_id)

    def get_response(self, payload: dict, session_id: str):  # noqa: PLR6301
        response = requests.post(
            url=f"/api/v1/chat/{session_id}/completion", json=payload, timeout=5
        )

        result = response.json()
        if response.status_code != 200:
            raise Exception(f"API returned status {response.status_code}: {response.text}")
        return result

    def save_message(self, payload: dict, session_id: str) -> None:  # noqa: PLR6301
        payload["id"] = session_id
        messages_json = json.dumps(payload, ensure_ascii=False)
        cache.set(session_id, messages_json, timeout=7200)

    async def get_history_chat(self, session_id: str):  # noqa: PLR6301
        messages = cache.get(session_id)
        if messages:
            return json.loads(messages)
        return {"error": "No messages found"}
