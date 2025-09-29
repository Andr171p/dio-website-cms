from typing import ClassVar

from django.db import models


# Create your models here.
class AddDocument(models.Model):
    page_content = models.TextField(
        verbose_name="Содержимое документа", help_text="Основной текстовый контент документа"
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Метаданные",
        help_text="Дополнительные метаданные в формате JSON",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Добавленые документы"
        ordering: ClassVar[list] = ["-created_at"]

    def __str__(self):
        return f"Добавленный документ номер{self.id}" # pyright: ignore[reportAttributeAccessIssue]  # noqa: E261


class UploadDocument(models.Model):
    file = models.FileField(
        upload_to="resumes/%Y/%m/%d/", verbose_name="Файл", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Загруженные документы"
        ordering: ClassVar[list] = ["-created_at"]

    def __str__(self):
        return f"Загруженный документ номер{self.id}" # pyright: ignore[reportAttributeAccessIssue]  # noqa: E261
