from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.search import index
from django.utils import timezone
from wagtail.blocks import (
    CharBlock, RichTextBlock, StructBlock, ListBlock, PageChooserBlock, ChoiceBlock
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail import blocks
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

SERVICE_CATEGORY_CHOICES = [
    ("consulting", "Консультации"),
    ("development", "Разработка"),
    ("design", "Дизайн"),
    ("support", "Поддержка"),
    ("training", "Обучение"),
    ("1c_services", "1С-сервисы"),  
]

class HeroBlock(StructBlock):
    title = CharBlock(required=True, label="Заголовок Hero")
    subtitle = CharBlock(required=True, label="Подзаголовок Hero")
    image = ImageChooserBlock(required=True, label="Изображение Hero")
    button_text = CharBlock(required=False, label="Текст кнопки")
    button_link = PageChooserBlock(required=False, label="Ссылка кнопки")

    class Meta:
        icon = "image"
        label = "Hero"

class TextBlock(StructBlock):
    content = RichTextBlock(
        features=['h2', 'h3', 'bold', 'italic', 'link', 'ol', 'ul', 'blockquote'],
        label="Текст"
    )

    class Meta:
        icon = "doc-full"
        label = "Текстовая секция"

class WhatWeDoBlock(StructBlock):
    title = CharBlock(required=True, label="Заголовок")
    description = RichTextBlock(required=True, label="Описание")
    image = ImageChooserBlock(required=True, label="Изображение слева")

    class Meta:
        icon = "edit"
        label = "Что мы делаем"

class ImageCardBlock(StructBlock):
    image = ImageChooserBlock(required=True, label="Изображение")
    title = CharBlock(required=True, label="Заголовок")
    description = RichTextBlock(required=False, label="Описание")
    button_text = CharBlock(required=False, label="Текст кнопки")
    button_link = PageChooserBlock(required=False, label="Ссылка кнопки")

    class Meta:
        icon = "image"
        label = "Карточка с изображением"

class CardItemBlock(StructBlock):
    title = CharBlock(required=True, label="Название")
    description = RichTextBlock(required=False, label="Описание")
    icon = ImageChooserBlock(required=False, label="Иконка (SVG)")
    image = ImageChooserBlock(required=False, label="Изображение")

    class Meta:
        icon = "pick"
        label = "Элемент карточки"

class CardGridBlock(StructBlock):
    title = CharBlock(required=True, label="Заголовок сетки")
    grid_type = ChoiceBlock(choices=[
        ('numbered', 'Нумерованный'),
        ('bulleted', 'Маркированный'),
        ('icon_grid', 'Сетка с иконками'),
        ('image_grid', 'Сетка с изображениями'),
    ], default='icon_grid', label="Тип сетки")
    items = ListBlock(CardItemBlock(), label="Элементы сетки")

    class Meta:
        icon = "folder-open"
        label = "Универсальная сетка карточек"

class MetricItemBlock(StructBlock):
    value = CharBlock(required=True, label="Значение (например, '10+', '100')")
    label = CharBlock(required=True, label="Описание (например, 'Лет на рынке')")
    icon = ImageChooserBlock(required=False, label="Иконка (SVG)")

    class Meta:
        icon = "pick"
        label = "Метрика"

class MetricsBlock(StructBlock):
    title = CharBlock(required=True, label="Заголовок метрик")
    items = ListBlock(MetricItemBlock(), label="Список метрик")

    class Meta:
        icon = "site"
        label = "Метрики доверия"

class GalleryBlock(StructBlock):
    title = CharBlock(required=False, label="Заголовок галереи")
    images = ListBlock(ImageChooserBlock(), label="Изображения")

    class Meta:
        icon = "image"
        label = "Галерея изображений"

class VideoBlock(StructBlock):
    title = CharBlock(required=False, label="Заголовок видео")
    video = EmbedBlock(required=True, label="Встраиваемое видео (YouTube, Vimeo и т.д.)")

    class Meta:
        icon = "media"
        label = "Видео"

class AccordionItemBlock(StructBlock):
    question = CharBlock(required=True, label="Вопрос/Заголовок")
    answer = RichTextBlock(required=True, label="Ответ/Описание")

    class Meta:
        icon = "help"
        label = "Элемент аккордеона"

class AccordionBlock(StructBlock):
    title = CharBlock(required=True, label="Заголовок аккордеона")
    items = ListBlock(AccordionItemBlock(), label="Элементы аккордеона")

    class Meta:
        icon = "list-ul"
        label = "Аккордеон (FAQ/Детали)"

class CTABlock(StructBlock):
    title = CharBlock(required=True, label="Заголовок CTA")
    description = RichTextBlock(required=True, label="Описание CTA")
    button_text = CharBlock(required=True, label="Текст кнопки")
    button_link = PageChooserBlock(required=False, label="Ссылка")

    class Meta:
        icon = "plus"
        label = "CTA"

class SupportedConfigurationItemBlock(StructBlock):
    name = CharBlock(required=True, label="Название конфигурации")
    version = CharBlock(required=False, label="Версия/Редакция")
    tested = ChoiceBlock(choices=[
        ('full', 'Полностью протестировано'),
        ('partial', 'Частично поддерживается'),
    ], default='full', label="Статус тестирования")
    description = RichTextBlock(required=False, label="Описание")

    class Meta:
        icon = "pick"
        label = "Конфигурация 1С"

class SupportedConfigurationsBlock(StructBlock):
    title = CharBlock(required=True, label="Заголовок блока конфигураций", default="Поддерживаемые конфигурации")
    items = ListBlock(SupportedConfigurationItemBlock(), label="Список конфигураций")

    class Meta:
        icon = "list-ul"
        label = "Поддерживаемые конфигурации 1С"

class SystemRequirementItemBlock(StructBlock):
    category = CharBlock(required=True, label="Категория (например, Платформа, ОС)")
    requirement = RichTextBlock(required=True, label="Требования")

    class Meta:
        icon = "cogs"
        label = "Элемент требований"

class SystemRequirementsBlock(StructBlock):
    title = CharBlock(required=True, label="Заголовок блока требований", default="Системные требования")
    items = ListBlock(SystemRequirementItemBlock(), label="Список требований")

    class Meta:
        icon = "cogs"
        label = "Системные требования"

class Single1CServicePage(Page):


    date = models.DateField("Дата публикации", default=timezone.now)
    category = models.CharField(
        max_length=100,
        choices=SERVICE_CATEGORY_CHOICES,
        default="1c_services",  
        verbose_name="Категория",
    )
    headline = models.CharField(
        "Заголовок", max_length=255, default="Заголовок сервиса 1С"
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
        ('text', TextBlock()),
        ('what_we_do', WhatWeDoBlock()),
        ('image_card', ImageCardBlock()),
        ('card_grid', CardGridBlock()),
        ('metrics', MetricsBlock()),
        ('gallery', GalleryBlock()),
        ('video', VideoBlock()),
        ('accordion', AccordionBlock()),
        ('cta', CTABlock()),
        ('supported_configurations', SupportedConfigurationsBlock()),  
        ('system_requirements', SystemRequirementsBlock()),  
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

    parent_page_types = ["services_1c.Service1CIndexPage"]
    subpage_types = []

    def get_context(self, request):
        context = super().get_context(request)
        context["other_1c_services"] = (
            Single1CServicePage.objects.live().exclude(id=self.id).order_by("-date")[:3]
        )
        return context

    class Meta:
        verbose_name = "Сервис 1С"
        verbose_name_plural = "Сервисы 1С"

class Service1CIndexPage(Page):


    intro = RichTextField("Введение", features=["bold", "italic", "link"], blank=True)
    items_per_page = models.PositiveIntegerField("Сервисов на странице", default=9)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("items_per_page"),
    ]

    subpage_types = ['services_1c.Single1CServicePage']
    parent_page_types = ['home.HomePage']
    
    def get_context(self, request):
        context = super().get_context(request)
        services = Single1CServicePage.objects.live().order_by("-date")
        category = request.GET.get("category")
        if category:
            services = services.filter(category=category)
        context["current_category"] = category

        paginator = Paginator(services, self.items_per_page)
        page = request.GET.get("page")
        try:
            services = paginator.page(page)
        except PageNotAnInteger:
            services = paginator.page(1)
        except EmptyPage:
            services = paginator.page(paginator.num_pages)

        context["1c_services"] = services
        context["SERVICE_CATEGORY_CHOICES"] = SERVICE_CATEGORY_CHOICES
        return context

    class Meta:
        verbose_name = "Лента сервисов 1С"
        verbose_name_plural = "Ленты сервисов 1С"

class Service1CBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        max_length=100, required=True, label="Заголовок секции сервисов 1С"
    )
    show_count = blocks.IntegerBlock(
        default=3, min_value=1, max_value=12, label="Количество сервисов для показа"
    )

    class Meta:
        icon = "doc-full"
        label = "Блок сервисов 1С"