from typing import ClassVar

from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page, PanelPlaceholder

MAX_CATEGORY_LENGTH = 250
PARAGRAPH_FEATURES: list[str] = [
    "h2", "h3", "h4", "bold", "italic", "link", "ol", "ul", "code", "blockquote"
]
NEWS_CATEGORY_CHOICES: list[tuple] = [
    ("company", "Новости компании"),
    ("tech", "Технологии"),
    ("projects", "Проекты"),
    ("events", "События"),
    ("awards", "Награды"),
]


class NewsPage(Page):
    """Новостная страница"""
    publish_date = models.DateField(auto_now_add=True, verbose_name="Дата публикации")
    headline = models.CharField(blank=True, verbose_name="Новостной заголовок")
    intro = models.TextField(
        blank=True, verbose_name="Краткое описание", help_text="1-3 предложения для анонса"
    )
    # Конструктор новостного контента
    content = StreamField([
        ("paragraph", blocks.RichTextBlock(
            features=PARAGRAPH_FEATURES,
            label="Абзац текста",
            template="blocks/paragraph_block.html",
        )),
        ("image", ImageChooserBlock(
            label="Изображение", template="blocks/image_block.html"
        )),
        ("quote", blocks.BlockQuoteBlock(
            label="Цитата", template="blocks/quote_block.html"
        )),
        ("embed", blocks.StaticBlock(
            label="Видео", template="blocks/embed_block.html"
        )),
        ("divider", blocks.StaticBlock(
            label="Разделитель", template="blocks/divider_block.html"
        ))
    ], use_json_field=True, verbose_name="Содержание новости", blank=True)
    # Мета информация
    category = models.CharField(
        max_length=MAX_CATEGORY_LENGTH,
        choices=NEWS_CATEGORY_CHOICES,
        default="company",
        verbose_name="Категория"
    )
    is_important = models.BooleanField(default=False, verbose_name="Важная новость")
    # Поля редактируемые админом
    content_panels: ClassVar[list[PanelPlaceholder]] = [
        *Page.content_panels,
        MultiFieldPanel([
            FieldPanel("headline"),
            FieldPanel("intro"),
            FieldPanel("category"),
            FieldPanel("is_important"),
        ], heading="Основная информация"),
        FieldPanel("content"),
    ]
    # Родительская страница

