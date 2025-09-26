from typing import ClassVar

from django.db import models
from django.utils import timezone
from modelcluster.models import ClusterableModel


class AdminNotification(ClusterableModel):
    title = models.CharField(verbose_name="Наименование")
    message = models.TextField(verbose_name="Сообщение")
    url = models.URLField(blank=True, null=True, verbose_name="Ссылка")  # Ссылка для уведомления
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    is_read = models.BooleanField(default=False, verbose_name="Просмотрено")

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
        ordering: ClassVar[list] = ["-created_at"]

    def __str__(self):
        return f"{self.message}"
