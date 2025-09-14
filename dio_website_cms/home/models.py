from typing import ClassVar

from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.fields import StreamField
from wagtail.models import Page, PanelPlaceholder

from .blocks import ContactsBlock, FeedbackFormBlock

MAX_HEADLINE_LENGTH = 100
MAX_SUBHEADLINE_LENGTH = 250


class HomePage(Page):
    """Лендинг сайта, главная страница"""
    hero_headline = models.CharField(
        max_length=MAX_HEADLINE_LENGTH,
        null=True,
        blank=True,
        verbose_name="Главный заголовок",
        help_text="Основной заголовок в верхней секции"
    )
    hero_subheadline = models.CharField(
        max_length=MAX_SUBHEADLINE_LENGTH,
        blank=True,
        verbose_name="Подзаголовок",
        help_text="Дополнительный текст под основным заголовком"
    )
    hero_background_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Фоновое изображение",
        help_text="Рекомендуемый размер: 1920x1080px"
    )
    content_blocks = StreamField([
        ("services_section", blocks.StructBlock([
            ("section_title", blocks.CharBlock(label="Заголовок секции")),
            ("services", blocks.ListBlock(blocks.PageChooserBlock(
                page_type="services.ServicePage"
            )))
        ], label="Предоставляемые услуги компании")),
        ("casestudies_section", blocks.StructBlock([
            ("section_title", blocks.CharBlock(label="Заголовок секции")),
            ("casestudies", blocks.ListBlock(blocks.PageChooserBlock(
                page_type="casestudies.CaseStudyPage"
            )))
        ], label="Кейсы (внедрения)")),
        ("solution_section", blocks.StructBlock([
            ("section_title", blocks.CharBlock(label="Заголовок секции")),
            ("solutions", blocks.ListBlock(blocks.PageChooserBlock(
                page_type="solutions.SolutionPage"
            )))
        ], label="Решения")),
        ("news_section", blocks.StructBlock([
            ("section_title", blocks.CharBlock(label="Новостной заголовок")),
            ("news", blocks.ListBlock(blocks.PageChooserBlock(
                page_type="news.NewsIndexPage"
            )))
        ], label="Новости")),
        ("contacts_section", ContactsBlock(label="Контакты компании")),
        ("feedback_form_section", FeedbackFormBlock(label="Форма обратной связи"))
    ], blank=True, use_json_field=True)

    content_panels: ClassVar[list[PanelPlaceholder]] = [
        *Page.content_panels,
        MultiFieldPanel([
            FieldPanel("hero_headline"),
            FieldPanel("hero_subheadline"),
            FieldPanel("hero_background_image"),
        ], heading="Главная секция"),
        FieldPanel("content_blocks"),
    ]
    # Поля отображаемые в API
    api_fields: ClassVar[list[APIField]] = [
        APIField("hero_headline"),
        APIField("hero_subheadline"),
        APIField("hero_background_image"),
        APIField("content_blocks"),
    ]
