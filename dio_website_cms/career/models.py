# career/models.py
from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index




class CareerPage(Page):
    template = "career/career_page.html"

    content = StreamField([
        # Герой
        ('hero', blocks.StructBlock([
            ('title', blocks.CharBlock(default="Присоединяйся к DIO")),
            ('subtitle', blocks.TextBlock(blank=True)),
            ('image', ImageChooserBlock(blank=True)),
            ('cta_text', blocks.CharBlock(default="Смотреть вакансии")),
            ('cta_scroll', blocks.BooleanBlock(default=True, help_text="Прокрутка к вакансиям")),
        ], icon="image")),

        # Текстовый раздел (для "О компании" и т.д.)
        ('text_section', blocks.StructBlock([
            ('title', blocks.CharBlock(default="О компании")),
            ('content', blocks.RichTextBlock(blank=True)),
            ('image', ImageChooserBlock(blank=True)),
        ], icon="doc-full")),

        # Ценности (любое количество пунктов)
        ('values', blocks.StructBlock([
            ('title', blocks.CharBlock(default="Наши ценности")),
            ('items', blocks.ListBlock(blocks.StructBlock([
                ('title', blocks.CharBlock()),
                ('description', blocks.TextBlock(blank=True)),
                ('icon', ImageChooserBlock(blank=True)),
            ]))),
        ], icon="list-ul")),

        # Вакансии
        ('vacancies_list', blocks.StructBlock([
            ('title', blocks.CharBlock(default="Открытые вакансии")),
        ], icon="user")),

        # Форма
        ('form', blocks.StructBlock([
            ('title', blocks.CharBlock(default="Хочешь к нам?")),
            ('description', blocks.TextBlock(blank=True)),
        ], icon="mail")),

        # Офис
        ('office', blocks.StructBlock([
            ('title', blocks.CharBlock(default="Наш офис")),
            ('address', blocks.CharBlock(blank=True)),
        ], icon="home")),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("content"),
    ]


    subpage_types = ['career.CareerVacancyPage']
    parent_page_types = ['home.HomePage']


    
    class Meta:
        verbose_name = "Страница 'Карьера'"
        verbose_name_plural = "Страницы 'Карьера'"

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.blocks import (
    CharBlock, RichTextBlock, StructBlock, ChoiceBlock,
    ListBlock, URLBlock, StreamBlock  # ← StreamBlock, а не StreamField!
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Image


class CareerVacancyPage(Page):
    template = "career/career_vacancy_page.html"

    # === ОСНОВНЫЕ ПОЛЯ ===
    department = models.CharField(max_length=100, default="Разработка")
    salary = models.CharField(max_length=100, blank=True, help_text="Например: от 150 000 ₽")
    location = models.CharField(max_length=100, default="Сыктывкар")
    work_format = models.CharField(
        max_length=50,
        choices=[("office", "Офис"), ("remote", "Удалённо"), ("hybrid", "Гибрид")],
        default="office"
    )
    

    # === HERO ===
    hero_image = models.ForeignKey(
        Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )

    # === КОНТЕНТ: Вложенный StreamField через StreamBlock ===
    content = StreamField([
        ("section", StructBlock([
            ("heading", CharBlock(default="Заголовок секции")),
            ("content", StreamBlock([  # ← StreamBlock, а не StreamField!
                ("paragraph", RichTextBlock(
                    features=['bold', 'italic', 'link', 'ol', 'ul', 'h3', 'h4'],
                    icon="pilcrow"
                )),
                ("image", StructBlock([
                    ("image", ImageChooserBlock()),
                    ("image_position", ChoiceBlock(
                        choices=[("left", "Слева"), ("right", "Справа")],
                        default="right"
                    )),
                    ("text_content", StructBlock([
                        ("heading", CharBlock()),
                        ("description", RichTextBlock()),
                        ("button_text", CharBlock(blank=True)),
                        ("button_url", URLBlock(blank=True)),
                    ])),
                ], icon="image")),
                ("image_carousel", ListBlock(
                    StructBlock([
                        ("image", ImageChooserBlock()),
                        ("caption", CharBlock(blank=True)),
                    ]), icon="image"
                )),
                ("image_grid", ListBlock(
                    StructBlock([
                        ("image", ImageChooserBlock()),
                        ("caption", CharBlock(blank=True)),
                    ]), icon="image"
                )),
                ("numbered_list", ListBlock(RichTextBlock(), icon="list-ol")),
                ("bullet_list", ListBlock(RichTextBlock(), icon="list-ul")),
                ("quote", StructBlock([
                    ("text", RichTextBlock()),
                    ("author", CharBlock(blank=True)),
                ], icon="openquote")),
                ("accordion", ListBlock(
                    StructBlock([
                        ("title", CharBlock()),
                        ("content", RichTextBlock()),
                    ]), icon="pilcrow"
                )),
                ("call_to_action", StructBlock([
                    ("title", CharBlock()),
                    ("description", RichTextBlock()),
                    ("button_text", CharBlock()),
                    ("button_url", URLBlock()),
                ], icon="mail")),
                ("cards", ListBlock(
                    StructBlock([
                        ("image", ImageChooserBlock(required=False)),
                        ("title", CharBlock()),
                        ("description", RichTextBlock()),
                        ("button_text", CharBlock(blank=True)),
                        ("button_url", URLBlock(blank=True)),
                    ]), icon="grip"
                )),
            ], use_json_field=True)),
        ], icon="folder-open")),
    ], use_json_field=True, blank=True)

    # === ПАНЕЛИ ===
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("title"),
            FieldPanel("department"),
            FieldPanel("salary"),
            FieldPanel("location"),
            FieldPanel("work_format"),
            FieldPanel("hero_image"),
        ], heading="Основная информация", classname="collapsible"),
        FieldPanel("content"),
    ]

    parent_page_types = ["career.CareerPage"]
    subpage_types = []

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"