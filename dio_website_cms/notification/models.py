from typing import ClassVar

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from modelcluster.models import ClusterableModel


class AdminNotification(ClusterableModel):
    message = models.TextField(verbose_name="Сообщение")
    url = models.URLField(blank=True, null=True, verbose_name="Ссылка")  # Ссылка для уведомления
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False, verbose_name="Обработано")

    class Meta:
        ordering: ClassVar[list] = ["-created_at"]

    def __str__(self):
        return f"{self.message[:50]}"
