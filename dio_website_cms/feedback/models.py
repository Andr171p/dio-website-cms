from typing import ClassVar

from django.db import models
from notification.utils import create_admin_notification
from wagtail.admin.panels import FieldPanel

from .utils import get_tumen_time


class FeedbackMessage(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    company = models.CharField(verbose_name="Компания", blank=True, null=True)
    service_of_interest = models.CharField(verbose_name="Интересующа услуга")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(default=get_tumen_time, verbose_name="Дата создания")
    is_processed = models.BooleanField(default=False, verbose_name="Обработано")

    panels: ClassVar[list[FieldPanel]] = [
        FieldPanel("name"),
        FieldPanel("email"),
        FieldPanel("phone"),
        FieldPanel("company"),
        FieldPanel("service_of_interest"),
        FieldPanel("message"),
        FieldPanel("is_processed"),
    ]

    class Meta:
        verbose_name = "Сообщение обратной связи"
        verbose_name_plural = "Сообщения обратной связи"
        ordering: ClassVar[list] = ["-created_at"]

    def __str__(self):
        return f"{self.email}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            create_admin_notification(
                message=f"Новое сообщение обратной связи от {self.email}",
                url=f"http://127.0.0.1:7000/admin/snippets/feedback/feedbackmessage/edit/{self.id}/",  # type: ignore  # noqa: PGH003
            )
