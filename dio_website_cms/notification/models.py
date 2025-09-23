from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from modelcluster.models import ClusterableModel


class AdminNotification(ClusterableModel):
    # Кому предназначено уведомление (None для всех)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    LEVEL_CHOICES = (
        ("info", "Информация"),
        ("warning", "Предупреждение"),
        ("success", "Успех"),
        ("error", "Ошибка"),
    )
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="info")
    message = models.TextField()
    url = models.URLField(blank=True, null=True)  # Ссылка для уведомления
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.level}: {self.message[:50]}"
