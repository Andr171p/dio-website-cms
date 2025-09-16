from typing import ClassVar

from rest_framework import serializers


class ChatMessageSerializer(serializers.Serializer):
    content = serializers.CharField(required=True)

    class Meta:
        fields: ClassVar[list] = ["content"]
