from typing import ClassVar

from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page

from .blocks import SolutionIntroBlock

MAX_ICON_LENGTH = 20
MAX_HEADLINE_LENGTH = 100
MAX_TAGLINE_LENGTH = 250


class SolutionPage(Page):
    """Страница с решением/продуктом компании"""
    headline = models.CharField(
        max_length=MAX_HEADLINE_LENGTH,
        blank=True,
        verbose_name="Название продукта/решения",
    )
    tagline = models.CharField(
        max_length=MAX_TAGLINE_LENGTH,
        blank=True,
        verbose_name="Слоган решения",
        help_text="Краткий слоган решения/продукта, например: 'Система автоматизации контроля ...'"
    )
    background_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Фоновое изображение для визитки продукта"
    )
    main_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Изображение с примером работы продукта",
        help_text="Рекомендуемый размер 1200x630px"
    )
    presentation_file = models.FileField(
        upload_to="presentations/",
        blank=True,
        null=True,
        verbose_name="Презентация",
        help_text="Презентация в формате PDF или PPTX"
    )
    intro = StreamField([
        ("intro_block", SolutionIntroBlock(label="Описание продукта")),
    ], blank=True, use_json_field=True, verbose_name="Блоки описания продукта")

    # Поля редактируемые админом
    content_panels: ClassVar[list[MultiFieldPanel | FieldPanel]] = [
        *Page.content_panels,
        MultiFieldPanel([
            FieldPanel("headline"),
            FieldPanel("tagline"),
        ], heading="Основная информация о продукте"),
    ]


class SolutionIndexPage(Page):
    """Страница со списком всех решений"""
    background_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    tagline = models.CharField(
        max_length=MAX_TAGLINE_LENGTH,
        blank=True,
        verbose_name="Слоган решения",
        help_text="Краткий слоган решения/продукта, например: 'Система автоматизации контроля ...'"
    )
    # Поля заполняемые в админ панели
    content_panels: ClassVar[list[FieldPanel]] = [
        *Page.content_panels,
        FieldPanel("background_image"),
        FieldPanel("tagline"),
    ]
    # Дочерние страницы
    subpage_types: ClassVar[list[str]] = ["SolutionPage"]
    # Родительская страница
    parent_page_types: ClassVar[list[str]] = ["home.HomePage"]
