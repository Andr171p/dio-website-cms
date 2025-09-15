from typing import Any, ClassVar

from django.db import models
from django.http import HttpRequest
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.search import index
from wagtail.search.index import SearchField


class CaseStudyPage(Page):
    """Успешные внедрения, кейсы"""
    customer_name = models.CharField(
        "Имя заказчика", max_length=100, blank=True
    )
    customer_logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Логотип заказчика"
    )
    industry = models.CharField(
        "Отрасль заказчика",
        max_length=50,
        blank=True,
        help_text="Например: Нефтегазовая, Промышленность"
    )
    intro = RichTextField(
        "Краткое описание",
        features=["bold", "italic"],
        max_length=250,
    )
    content = StreamField([
        ("about_customer", blocks.StructBlock([
            ("title", blocks.CharBlock(label="Заголовок", default="О заказчике")),
            ("content", blocks.RichTextBlock(
                label="Содержание", features=["bold", "italic", "link"]
            )),
        ], icon="user", label="О заказчике")),
        ("purpose", blocks.StructBlock([
            ("title", blocks.CharBlock(label="Заголовок", default="Цель внедрения")),
            ("content", blocks.RichTextBlock(label="Содержание")),
        ], icon="target", label="Цель внедрения")),
        ("automation_fields", blocks.StructBlock([
            ("title", blocks.CharBlock(label="Заголовок", default="Области автоматизации")),
            ("content", blocks.RichTextBlock(label="Содержание")),
            ("fields_list", blocks.ListBlock(
                blocks.CharBlock(label="Область"),
                label="Список областей"
            )),
        ], icon="cog", label="Области автоматизации")),
        ("metrics", blocks.StructBlock([
            ("title", blocks.CharBlock(label="Заголовок", default="Результаты внедрения")),
            ("metrics_list", blocks.ListBlock(
                blocks.StructBlock([
                    ("value", blocks.CharBlock(
                        label="Значение (%)", help_text="Например: 19.6"
                    )),
                    ("description", blocks.CharBlock(
                        label="Описание", help_text="Например: сократили расходы"
                    )),
                    ("icon", blocks.ChoiceBlock(
                        choices=[
                            ("arrow-up", "Рост"),
                            ("arrow-down", "Сокращение"),
                        ],
                        label="Тип изменения"
                    )),
                ], label="Метрика"),
                label="Список метрик"
            )),
        ], icon="chart-bar", label="Метрики эффективности")),
        ("problems", blocks.StructBlock([
            ("title", blocks.CharBlock(label="Заголовок", default="Проблемы и сложности")),
            ("content", blocks.RichTextBlock(label="Содержание")),
            ("problems_list", blocks.ListBlock(
                blocks.CharBlock(label="Проблема"),
                label="Список проблем"
            )),
        ], icon="warning", label="Проблемы")),
        ("progress", blocks.StructBlock([
            ("title", blocks.CharBlock(label="Заголовок", default="Ход реализации")),
            ("stages", blocks.ListBlock(
                blocks.StructBlock([
                    ("stage", blocks.CharBlock(label="Этап")),
                    ("description", blocks.TextBlock(label="Описание", required=False)),
                ], label="Этап"),
                label="Этапы реализации"
            )),
        ], icon="list-ol", label="Ход реализации")),
        ("results", blocks.StructBlock([
            ("title", blocks.CharBlock(label="Заголовок", default="Результаты")),
            ("content", blocks.RichTextBlock(label="Содержание")),
            ("subsystems", blocks.ListBlock(
                blocks.CharBlock(label="Подсистема"),
                label="Внедренные подсистемы"
            )),
        ], icon="check-circle", label="Результаты")),
        ("image", ImageChooserBlock(label="Изображение")),
        ("quote", blocks.BlockQuoteBlock(label="Цитата")),
    ], block_counts={
        "about_customer": {"min_num": 1, "max_num": 1},
        "purpose": {"min_num": 1, "max_num": 1},
    }, use_json_field=True, blank=True, verbose_name="Содержание кейса")

    # Поля для поиска
    search_fields: ClassVar[list[SearchField]] = [
        *Page.search_fields,
        index.SearchField("customer_name"),
        index.SearchField("industry"),
        index.SearchField("intro"),
        index.SearchField("content")
    ]

    # Панели редактирования
    content_panels: ClassVar[list[MultiFieldPanel | FieldPanel]] = [
        *Page.content_panels,
        MultiFieldPanel([
            FieldPanel("customer_name"),
            FieldPanel("customer_logo"),
            FieldPanel("industry"),
        ],
            heading="Информация о заказчике"),
        FieldPanel("intro"),
        FieldPanel("content")]

    # Настройки родительских/дочерних страниц
    parent_page_types: ClassVar[list[str]] = ["CaseStudyIndexPage"]
    subpage_types: ClassVar[list[str]] = []

    class Meta:
        verbose_name = "Кейс внедрения"
        verbose_name_plural = "Кейсы внедрений"

    def __str__(self) -> str:
        return f"{self.customer_name} - {self.title}"


class CaseStudyIndexPage(Page):
    """Страница со списком всех кейсов"""
    customer_name = models.CharField(
        "Имя заказчика", max_length=250, blank=True
    )
    customer_logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Логотип заказчика"
    )
    intro = RichTextField(
        "Краткое описание",
        features=["bold", "italic"],
        max_length=250,
    )
    # Поля заполняемые в админ панели
    content_panels: ClassVar[list[FieldPanel]] = [
        *Page.content_panels,
        FieldPanel("customer_name"),
        FieldPanel("customer_logo"),
        FieldPanel("intro")
    ]
    # Ограничение типов дочерних страниц - только кейсы
    subpage_types: ClassVar[list[str]] = ["CaseStudyPage"]
    # Определение места создания индекса
    parent_page_types: ClassVar[list[str]] = ["home.HomePage"]

    def get_context(
            self, request: HttpRequest, *args, **kwargs  # noqa: ARG002
    ) -> dict[str, Any]:
        context = super().get_context(request)
        # Получаем все опубликованные кейсы
        casestudies = self.get_children().live().public().order_by("-first_published_at")
        context["cases"] = casestudies
        return context
