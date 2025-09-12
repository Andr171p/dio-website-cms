from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.search import index


class CasePage(Page):
    """Успешные внедрения, кейсы"""
    customer_name = models.CharField("Имя заказчика", max_length=250, blank=True)
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
        max_length=250
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
    search_fields = [  # noqa: RUF012
        *Page.search_fields,
        index.SearchField("customer_name"),
        index.SearchField("intro"),
        index.SearchField("content")
    ]

    # Панели редактирования
    content_panels = [  # noqa: RUF012
        *Page.content_panels,
        MultiFieldPanel([
            FieldPanel("customer_name"),
            FieldPanel("customer_logo")],
            heading="Информация о заказчике"),
        FieldPanel("intro"),
        FieldPanel("content")]

    # Настройки родительских/дочерних страниц
    parent_page_types = ["cases.CasesIndexPage"]  # noqa: RUF012
    subpage_types = []  # noqa: RUF012

    class Meta:
        verbose_name = "Кейс внедрения"
        verbose_name_plural = "Кейсы внедрений"


class CasesIndexPage(Page):
    """Страница со списком всех кейсов"""
    intro = RichTextField("Введение", features=["bold", "italic", "link"], blank=True)
    content_panels = [*Page.content_panels, FieldPanel("intro")]  # noqa: RUF012

    def get_context(self, request):
        context = super().get_context(request)
        # Получаем все опубликованные кейсы
        cases = CasePage.objects.live().public().order_by("-first_published_at")
        context["cases"] = cases
        return context

    subpage_types = ["CasePage"]  # noqa: RUF012
    parent_page_types = ["home.HomePage"]  # noqa: RUF012
