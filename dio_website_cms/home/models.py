from typing import ClassVar
from django.db import models
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.fields import StreamField
from wagtail.models import Page

from .blocks import ContactsBlock, FeedbackFormBlock

MAX_HEADLINE_LENGTH = 100
MAX_SUBHEADLINE_LENGTH = 250


class HeroSlideBlock(blocks.StructBlock):
    """Блок для слайдов hero-секции"""
    headline = blocks.CharBlock(
        max_length=MAX_HEADLINE_LENGTH,
        required=True,
        label="Заголовок слайда"
    )
    subheadline = blocks.CharBlock(
        max_length=MAX_SUBHEADLINE_LENGTH,
        required=False,
        label="Подзаголовок слайда"
    )
    background_image = ImageChooserBlock(
        required=True,
        label="Фоновое изображение",
        help_text="Рекомендуемый размер: 1920x1080px"
    )
    link = blocks.PageChooserBlock(
        required=False,
        label="Ссылка слайда"
    )

    class Meta:
        icon = 'image'
        label = "Слайд героя"


class HomePage(Page):
    """Лендинг сайта, главная страница с каруселью"""
    hero_slides = StreamField([
        ("slide", HeroSlideBlock(label="Слайд"))
    ], blank=True, use_json_field=True, verbose_name="Слайды героя")

    content_blocks = StreamField([
        ("services_section", blocks.StructBlock([
            ("section_title", blocks.CharBlock(label="Заголовок секции")),
            ("services", blocks.ListBlock(blocks.PageChooserBlock(
                page_type="services.ServicePage"
            )))
        ], label="Предоставляемые услуги компании")),
        ("casestudies_section", blocks.StructBlock([
            ("section_title", blocks.CharBlock(label="Заголовок секции")),
            ("cases", blocks.ListBlock(blocks.PageChooserBlock(
                page_type="cases.CaseStudyPage"
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

    content_panels: ClassVar[list] = [
        *Page.content_panels,
        MultiFieldPanel([
            FieldPanel("hero_slides"),
        ], heading="Главная карусель"),
        FieldPanel("content_blocks"),
    ]

    api_fields: ClassVar[list[APIField]] = [
        APIField("hero_slides"),
        APIField("content_blocks"),
    ]