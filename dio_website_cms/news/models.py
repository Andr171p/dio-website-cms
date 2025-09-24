from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.search import index
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail import blocks

# Константы для категорий
NEWS_CATEGORY_CHOICES = [
    ("company", "Новости компании"),
    ("tech", "Технологии"),
    ("projects", "Проекты"),
    ("events", "События"),
    ("awards", "Награды"),
]


class NewsPage(Page):
    """Страница отдельной новости"""

    date = models.DateField("Дата публикации", default=timezone.now)
    category = models.CharField(
        max_length=100,
        choices=NEWS_CATEGORY_CHOICES,
        default="company",
        verbose_name="Категория",
    )
    headline = models.CharField(
        "Заголовок", max_length=255, default="Заголовок новости"
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
    content = RichTextField("Содержание", blank=True)

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
        FieldPanel("content"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("headline"),
        index.SearchField("intro"),
        index.SearchField("content"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        # Другие новости (исключая текущую)
        context["other_news"] = (
            NewsPage.objects.live().exclude(id=self.id).order_by("-date")[:3]
        )
        return context

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class NewsIndexPage(Page):
    """Главная страница новостей"""

    intro = RichTextField("Введение", features=["bold", "italic", "link"], blank=True)
    items_per_page = models.PositiveIntegerField("Новостей на странице", default=9)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("items_per_page"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        news = NewsPage.objects.live().order_by("-date")
        category = request.GET.get("category")
        if category:
            news = news.filter(category=category)
        context["current_category"] = category

        # Пагинация
        paginator = Paginator(news, self.items_per_page)
        page = request.GET.get("page")
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)

        context["news"] = news
        context["NEWS_CATEGORY_CHOICES"] = NEWS_CATEGORY_CHOICES
        return context

    class Meta:
        verbose_name = "Лента новостей"
        verbose_name_plural = "Ленты новостей"


# Блок для отображения новостей на главной
class NewsBlock(blocks.StructBlock):
    """Блок для отображения новостей на главной странице"""

    title = blocks.CharBlock(
        max_length=100, required=True, label="Заголовок секции новостей"
    )
    show_count = blocks.IntegerBlock(
        default=3, min_value=1, max_value=12, label="Количество новостей для показа"
    )

    class Meta:
        icon = "doc-full"
        label = "Блок новостей"
