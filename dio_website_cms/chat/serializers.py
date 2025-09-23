from typing import ClassVar

from rest_framework import serializers


class ChatMessageSerializer(serializers.Serializer):
    content = serializers.CharField(required=True)

    class Meta:
        fields: ClassVar[list] = ["content"]


class AddDocumentSerializer(serializers.Serializer):
<<<<<<< HEAD
    text = serializers.CharField(required=True)
=======
    text = serializers.DictField(required=True)
>>>>>>> b17fa042fdb595f90e37f79bb887188aa444b013

    class Meta:
        fields: ClassVar[list] = ["text"]


class DeleteDocumentSerializer(serializers.Serializer):
    ids = serializers.ListField(required=True)

    class Meta:
<<<<<<< HEAD
        fields: ClassVar[list] = ["ids"]
=======
        fields: ClassVar[list] = ["ids"]
>>>>>>> b17fa042fdb595f90e37f79bb887188aa444b013
