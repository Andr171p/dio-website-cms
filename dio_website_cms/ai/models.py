from typing import ClassVar

import uuid

from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.db import models
from wagtail import blocks
from wagtail.fields import StreamField

from .rest import add_document, upload_document


class AddDocument(models.Model):
    page_content = models.TextField(
        verbose_name="Содержимое документа", help_text="Основной текстовый контент документа"
    )
    metadata = StreamField(
        [
            (
                "metadata",
                blocks.ListBlock(
                    blocks.StructBlock([
                        ("key", blocks.CharBlock(required=True, label="Название", max_length=255)),
                        (
                            "value",
                            blocks.CharBlock(required=True, label="Содержание", max_length=500),
                        ),
                    ]),
                    label="Метаданные",
                    help_text="Добавляйте элементы метаданных",
                ),
            )
        ],
        use_json_field=True,
        blank=True,
        max_num=1,  # ← Только один блок метаданных
        verbose_name="Метаданные документа",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Добавленные документы"
        ordering: ClassVar[list] = ["-created_at"]

    def __str__(self):
        return f"Добавленный документ номер {self.id}"  # pyright: ignore[reportAttributeAccessIssue]

    def save(self, *args, **kwargs):
        if not self.pk and not self.page_content and not self.metadata:
            super().save(*args, **kwargs)
            return
        temp_id = str(uuid.uuid4()) if not self.pk else str(self.id)
        metadata_data = {}
        if self.metadata:
            for item in self.metadata:
                if item.block_type == "metadata":
                    for key_value in item.value:
                        metadata_data[key_value["key"]] = key_value
        print(metadata_data)
        payload = {
            "id": str(temp_id),
            "page_content": self.page_content,
            "metadata": metadata_data,
            "type": "Document",
        }
        add_document(payload)
        super().save(*args, **kwargs)


class UploadDocument(models.Model):
    file = models.FileField(upload_to="upload/%Y/%m/%d/", verbose_name="Файл")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Загруженные документы"
        ordering: ClassVar[list] = ["-created_at"]

    def __str__(self):
        return f"Загруженный документ номер{self.id}"  # pyright: ignore[reportAttributeAccessIssue]

    def clean(self):
        """Проверка расширения файла перед сохранением."""
        if self.file:
            file_extension = self.file.name.split(".")[-1].lower()
            allowed_extensions = ["pdf", "docx", "doc", "txt", "md"]
            if file_extension not in allowed_extensions:
                raise ValidationError(
                    f"Недопустимое расширение файла. Допустимы только: {', '.join(allowed_extensions)}"
                )

    def save(self, *args, **kwargs):
        if not self.pk and not self.file:
            super().save(*args, **kwargs)
            return

        self.clean()
        result = upload_document(self.file)
        if result:
            super().save(*args, **kwargs)
        else:
            self.file = None

    def delete(self, *args, **kwargs):
        # Удаляем файл перед удалением объекта
        if self.file:
            default_storage.delete(self.file.name)
        super().delete(*args, **kwargs)
