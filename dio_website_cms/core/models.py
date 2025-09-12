from typing import ClassVar

from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

from .constants import MAX_CHARS_LENGTH, MAX_CONTACT_LENGTH, MAX_ICON_LENGTH


@register_snippet
class Contact(models.Model):
    """Контакты компании"""
    CONTACT_TYPE_CHOICES: ClassVar[list[tuple]] = [
        ("phone", "Телефон"),
        ("email", "Email"),
        ("address", "Адрес"),
        ("whatsapp", "Whatsapp"),
        ("telegram", "Telegram"),
        ("other", "Другое"),
    ]

    contact_type = models.CharField(
        max_length=MAX_CONTACT_LENGTH, choices=CONTACT_TYPE_CHOICES, verbose_name="Тип контакта"
    )
    value = models.CharField(max_length=MAX_CHARS_LENGTH, verbose_name="Значение")
    label = models.CharField(
        max_length=MAX_CONTACT_LENGTH,
        blank=True,
        verbose_name="Подпись контакта",
        help_text="Например: 'Основной телефон', 'Электронная почта'"
    )
    icon = models.CharField(
        max_length=MAX_ICON_LENGTH,
        blank=True,
        verbose_name="Иконка",
        help_text="Название иконки (например: 'phone', 'email')"
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name="Основной контакт"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок отображения"
    )

    panels: ClassVar[list[FieldPanel]] = [
        FieldPanel("contact_type"),
        FieldPanel("value"),
        FieldPanel("label"),
        FieldPanel("icon"),
        FieldPanel("is_primary"),
        FieldPanel("order"),
    ]

    def __str__(self) -> str:
        return f"{self.get_contact_type_display()}: {self.value}"

    class Meta:
        verbose_name = "Контакт компании"
        verbose_name_plural = "Контакты компании"
        ordering: ClassVar[list[str]] = ["order", "contact_type"]
