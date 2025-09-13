from core.constants import MAX_ICON_LENGTH
from django.db import models
from wagtail.fields import RichTextField
from wagtail.models import Page


class SolutionPage(Page):
    """Решения компании"""
    icon = models.CharField(
        max_length=MAX_ICON_LENGTH,
        blank=True,
        verbose_name="Иконка"
    )
    short_description = RichTextField(
        blank=True, verbose_name="Краткое описание", help_text="Описание для карточек и списков"
    )
