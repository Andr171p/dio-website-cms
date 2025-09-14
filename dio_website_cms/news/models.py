from typing import Any, ClassVar

from django.core.paginator import PageNotAnInteger, Paginator
from django.db import models
from django.http import HttpRequest
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page, PanelPlaceholder

MAX_CATEGORY_LENGTH = 250
PARAGRAPH_FEATURES: list[str] = [
    "h2", "h3", "h4", "bold", "italic", "link", "ol", "ul", "code", "blockquote"
]
DEFAULT_NEWS_PER_PAGE = 6
FIRST_PAGE = 1
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
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Превью"
    )
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
    parent_page_types: ClassVar[list[str]] = ["NewsIndexPage"]
    subpage_types: ClassVar[list[str]] = []

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self) -> str:
        return f"{self.headline} - {self.title}"


class NewsIndexPage(Page):
    """Страница со списком всех новостей"""
    publish_date = models.DateField(auto_now_add=True, verbose_name="Дата публикации")
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Превью"
    )
    headline = models.CharField(blank=True, verbose_name="Новостной заголовок")
    news_per_page = models.PositiveIntegerField(
        default=DEFAULT_NEWS_PER_PAGE, verbose_name="Количество новостей на странице"
    )
    # Поля заполняемые админом
    content_panels: ClassVar[list[PanelPlaceholder]] = [
        *Page.content_panels,
        FieldPanel("image"),
        FieldPanel("headline"),
        FieldPanel("news_per_page"),
    ]
    # Дочерние страницы
    subpage_types: ClassVar[list[str]] = ["NewsPage"]
    # Родительская страница
    parent_page_types: ClassVar[list[str]] = ["home.HomePage"]

    def get_context(
            self, request: HttpRequest, *args, **kwargs  # noqa: ARG002
    ) -> dict[str, Any]:
        context = super().get_context(request)
        # Получаем все опубликованные новости
        news = NewsPage.objects.live().descendant_of(self).order_by("-publish_date")
        # Фильтрация по категориям
        category = request.GET.get("category")
        if category:
            news = news.filter(category=category)
        if not category:
            news = news.order_by("-is_important", "-publish_date")
        # Пагинация результатов
        page = request.GET.get("page")
        paginator = Paginator(news, self.news_per_page)
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(FIRST_PAGE)
        context["news"] = news
        context["current_category"] = category
        return context
