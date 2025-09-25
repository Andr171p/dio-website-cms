from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.search import index
from django.utils import timezone
from wagtail.fields import StreamField
from wagtail.api import APIField
from wagtail.blocks import (
    CharBlock, RichTextBlock, StructBlock, ListBlock, PageChooserBlock
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Константы для категорий услуг
SERVICE_CATEGORY_CHOICES = [
    ("consulting", "Консультации"),
    ("development", "Разработка"),
    ("design", "Дизайн"),
    ("support", "Поддержка"),
    ("training", "Обучение"),
]

# Блок для Hero
class HeroBlock(StructBlock):
    title = CharBlock(required=True, label="Заголовок Hero")
    subtitle = CharBlock(required=True, label="Подзаголовок Hero")
    image = ImageChooserBlock(required=True, label="Изображение Hero")

    class Meta:
        icon = "image"
        label = "Hero"

# Блок для "Что мы делаем"
class WhatWeDoBlock(StructBlock):
    title = CharBlock(required=True, label="Заголовок")
    description = RichTextBlock(required=True, label="Большой текст справа")
    svg_image = ImageChooserBlock(required=True, label="SVG/изображение слева")

    class Meta:
        icon = "edit"
        label = "Что мы делаем"

# Блок для больших квадратных изображений
class SquareImageBlock(StructBlock):
    image = ImageChooserBlock(required=True, label="Квадратное изображение")
    alt_text = CharBlock(required=False, label="Альтернативный текст")

    class Meta:
        icon = "image"
        label = "Квадратный блок изображения"

# Блок для сетки отраслей/услуг
class ExpertiseGridBlock(StructBlock):
    title = CharBlock(required=True, label="Заголовок сетки")
    items = ListBlock(CharBlock(label="Элемент сетки"), label="Список отраслей/услуг")

    class Meta:
        icon = "folder-open"
        label = "Сетка отраслей/услуг"

# Блок для CTA
class CTABlock(StructBlock):
    title = CharBlock(required=True, label="Заголовок CTA")
    description = RichTextBlock(required=True, label="Описание CTA")
    link_text = CharBlock(required=True, label="Текст кнопки")
    link_page = PageChooserBlock(required=False, label="Ссылка")

    class Meta:
        icon = "plus"
        label = "CTA"

class SingleServicePage(Page):
    date = models.DateField("Дата публикации", default=timezone.now)
    category = models.CharField(
        max_length=100,
        choices=SERVICE_CATEGORY_CHOICES,
        default="consulting",
        verbose_name="Категория",
    )
    headline = models.CharField(
        "Заголовок", max_length=255, default="Заголовок услуги"
    )
    intro = models.TextField(
        "Краткое описание", blank=True, help_text="1-3 предложения для анонса"
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Изображение",
    )
    content = StreamField([
        ('hero', HeroBlock()),
        ('what_we_do', WhatWeDoBlock()),
        ('square_image', SquareImageBlock()),
        ('expertise_grid', ExpertiseGridBlock()),
        ('cta', CTABlock()),
    ], blank=True, use_json_field=True, verbose_name="Блоки страницы")

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("date"),
                FieldPanel("category"),
                FieldPanel("headline"),
                FieldPanel("intro"),
                FieldPanel("image"),
            ],
            heading="Основная информация",
        ),
        MultiFieldPanel([
            FieldPanel('content'),
        ], heading="Блоки страницы"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("headline"),
        index.SearchField("intro"),
        index.SearchField("content"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        # Другие услуги (исключая текущую)
        context["other_services"] = (
            SingleServicePage.objects.live().exclude(id=self.id).order_by("-date")[:3]
        )
        return context

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

class ServiceIndexPage(Page):
    """Главная страница услуг"""

    intro = RichTextField("Введение", features=["bold", "italic", "link"], blank=True)
    items_per_page = models.PositiveIntegerField("Услуг на странице", default=9)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("items_per_page"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        services = SingleServicePage.objects.live().order_by("-date")
        category = request.GET.get("category")
        if category:
            services = services.filter(category=category)
        context["current_category"] = category

        # Пагинация
        paginator = Paginator(services, self.items_per_page)
        page = request.GET.get("page")
        try:
            services = paginator.page(page)
        except PageNotAnInteger:
            services = paginator.page(1)
        except EmptyPage:
            services = paginator.page(paginator.num_pages)

        context["services"] = services
        context["SERVICE_CATEGORY_CHOICES"] = SERVICE_CATEGORY_CHOICES
        return context

    class Meta:
        verbose_name = "Лента услуг"
        verbose_name_plural = "Ленты услуг"

# Блок для отображения услуг на главной
class ServiceBlock(blocks.StructBlock):
    """Блок для отображения услуг на главной странице"""

    title = blocks.CharBlock(
        max_length=100, required=True, label="Заголовок секции услуг"
    )
    show_count = blocks.IntegerBlock(
        default=3, min_value=1, max_value=12, label="Количество услуг для показа"
    )

    class Meta:
        icon = "doc-full"
        label = "Блок услуг"