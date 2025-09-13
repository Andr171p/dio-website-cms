from typing import ClassVar

from core.constants import MAX_CHARS_LENGTH, MAX_ICON_LENGTH, MAX_LABEL_LENGTH
from django.db import models
from wagtail.models import Page


class ServicePage(Page):
    """Услуги компании"""
    SERVICE_CATEGORY_CHOICES: ClassVar[list[tuple]] = [
        ("consulting", "Консалтинг и автоматизация"),
        ("development", "Разработка"),
        ("support", "Сопровождение 1С"),
        ("education", "Обучение 1С"),
    ]

    icon = models.CharField(
        max_length=MAX_ICON_LENGTH,
        blank=True,
        verbose_name="Иконка услуги",
        help_text="Название иконки (например: cog, chart-line, users)"
    )
    category = models.CharField(
        max_length=MAX_LABEL_LENGTH,
        choices=SERVICE_CATEGORY_CHOICES,
        default="consulting",
        verbose_name="Категория услуг"
    )
    short_description = models.CharField(
        max_length=MAX_CHARS_LENGTH,
        blank=True,
        verbose_name="Краткое описание",
        help_text="Короткое описание для карточек и списков"
    )
