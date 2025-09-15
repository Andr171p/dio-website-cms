from typing import ClassVar

from django.db import models
from wagtail.fields import RichTextField
from wagtail.models import Page


class ServicePage(Page):
    """Услуги компании"""
    SERVICE_CATEGORY_CHOICES: ClassVar[list[tuple]] = [
        ("consulting", "Консалтинг и автоматизация"),
        ("development", "Разработка"),
        ("support", "Сопровождение 1С"),
        ("education", "Обучение 1С"),
    ]

    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Фото-карточка услуги"
    )
    category = models.CharField(
        max_length=100,
        choices=SERVICE_CATEGORY_CHOICES,
        default="consulting",
        verbose_name="Категория услуг"
    )
    intro = RichTextField(
        features=["bold", "italic", "link"],
        verbose_name="Краткое описание услуги",
        blank=True,
    )
