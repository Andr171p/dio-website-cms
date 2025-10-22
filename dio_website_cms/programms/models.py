from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import (
    CharBlock, RichTextBlock, StructBlock, ListBlock, StreamBlock, RawHTMLBlock
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.contrib.table_block.blocks import TableBlock


# ------------------------------------------
# Базовые составные блоки 
# ------------------------------------------

class NumberedListBlock(StructBlock):
    items = ListBlock(
        RichTextBlock(features=['bold', 'italic'], help_text="Элемент списка.")
    )

    class Meta:
        icon = "list-ol"
        label = "Нумерованный список"


class BulletListBlock(StructBlock):
    items = ListBlock(
        RichTextBlock(features=['bold', 'italic'], help_text="Элемент списка.")
    )

    class Meta:
        icon = "list-ul"
        label = "Маркированный список"


class ImageCarouselBlock(ListBlock):
    def __init__(self, **kwargs):
        super().__init__(
            StructBlock([
                ('image', ImageChooserBlock(help_text="Изображение для карусели.")),
                ('caption', CharBlock(required=False, help_text="Подпись к изображению.")),
            ]),
            verbose_name="Карусель изображений",
            help_text="Список изображений для карусели.",
            **kwargs
        )


class ImageGridBlock(ListBlock):
    def __init__(self, **kwargs):
        super().__init__(
            StructBlock([
                ('image', ImageChooserBlock(help_text="Изображение для сетки.")),
                ('caption', CharBlock(required=False, help_text="Подпись к изображению.")),
            ]),
            verbose_name="Сетка изображений",
            help_text="Сетка изображений с подписями.",
            **kwargs
        )


class CardsBlock(ListBlock):
    def __init__(self, **kwargs):
        super().__init__(
            StructBlock([
                ('title', CharBlock(help_text="Заголовок карточки.")),
                ('image', ImageChooserBlock(required=False, help_text="Изображение для карточки.")),
                ('description', RichTextBlock(help_text="Описание карточки.")),
                ('button_text', CharBlock(required=False, help_text="Текст кнопки.")),
                ('button_url', CharBlock(required=False, help_text="URL для кнопки.")),
            ]),
            verbose_name="Карточки",
            help_text="Сетка карточек с заголовком, изображением и описанием.",
            **kwargs
        )


# ------------------------------------------
# Универсальный блок секции 
# ------------------------------------------

class SectionBlock(StructBlock):
    heading = CharBlock(
        verbose_name="Заголовок секции",
        help_text="Например: 'Описание', 'Преимущества', 'Основная информация'."
    )

    content = StreamBlock([
        ("paragraph", RichTextBlock(features=["bold", "italic", "ol", "ul", "link", "superscript"], label="Параграф")),
        ("image", StructBlock([
            ("image", ImageChooserBlock(
                help_text="Изображение для секции.",
                required=True
            )),
            ("image_position", CharBlock(
                choices=[
                    ("left", "Left"),
                    ("right", "Right")
                ],
                default="right",
                help_text="Image position (Left or Right)."
            )),
            ("text_content", StructBlock([
                ("heading", CharBlock(
                    help_text="Heading text.",
                    required=True
                )),
                ("description", RichTextBlock(
                    features=["bold", "italic", "ol", "ul", "link", "superscript"],
                    help_text="Description text.",
                    required=False
                )),
                ("button_text", CharBlock(
                    default="",
                    help_text="Button text.",
                    required=False
                )),
                ("button_url", CharBlock(
                    help_text="Button URL.",
                    required=False
                )),
            ], help_text="Text content block.", required=True, default={"heading": "Default Heading"}))
        ], verbose_name="Image with Text", help_text="Block with image and text on the left or right.", default={"image": None, "image_position": "right", "text_content": {"heading": "Default Heading"}})),
        ("image_carousel", ImageCarouselBlock()),
        ("image_grid", ImageGridBlock()),
        ("table", TableBlock(label="Таблица")),
        ("numbered_list", NumberedListBlock()),
        ("bullet_list", BulletListBlock()),
        ("quote", StructBlock([
            ("text", RichTextBlock(help_text="Текст цитаты.")),
            ("author", CharBlock(required=False, help_text="Автор цитаты.")),
        ], verbose_name="Цитата", icon="openquote")),
        ("embed", EmbedBlock(verbose_name="Видео")),
        ("raw_html", RawHTMLBlock(verbose_name="HTML-код")),
        ("button", StructBlock([
            ("text", CharBlock(default="Нажмите здесь", help_text="Текст кнопки.")),
            ("url", CharBlock(help_text="URL для кнопки.")),
        ], verbose_name="Кнопка", icon="link")),
        ("accordion", ListBlock(
            StructBlock([
                ("title", CharBlock(help_text="Заголовок аккордеона.")),
                ("content", RichTextBlock(help_text="Содержимое аккордеона.")),
            ]),
            verbose_name="Аккордеон",
            help_text="Раскрывающиеся секции."
        )),
        ("tabs", ListBlock(
            StructBlock([
                ("title", CharBlock(help_text="Заголовок вкладки.")),
                ("content", RichTextBlock(help_text="Содержимое вкладки.")),
            ]),
            verbose_name="Вкладки",
            help_text="Переключаемые вкладки."
        )),
        ("call_to_action", StructBlock([
            ("title", CharBlock(help_text="Заголовок призыва к действию.")),
            ("description", RichTextBlock(help_text="Описание призыва к действию.")),
            ("button_text", CharBlock(default="Узнать больше", help_text="Текст кнопки.")),
            ("button_url", CharBlock(help_text="URL для кнопки.")),
        ], verbose_name="Призыв к действию", icon="pick")),
        ("divider", StructBlock([], verbose_name="Разделитель")),
        ("spoiler", StructBlock([
            ("title", CharBlock(help_text="Заголовок спойлера.")),
            ("content", RichTextBlock(help_text="Содержимое спойлера.")),
        ], verbose_name="Спойлер", icon="collapse")),
        ("cards", CardsBlock()),
        ("document", DocumentChooserBlock(icon="doc-full", verbose_name="Документ")),
        ("metrics", StructBlock([
            ("items", ListBlock(
                StructBlock([
                    ("icon", ImageChooserBlock(required=False, help_text="Иконка для метрики.")),
                    ("value", CharBlock(help_text="Числовое значение метрики.")),
                    ("label", CharBlock(help_text="Подпись к метрике.")),
                ])
            )),
        ], verbose_name="Метрики", icon="table")),
    ], verbose_name="Содержимое секции", required=False)

    class Meta:
        icon = "placeholder"
        label = "Секция с заголовком"
        help_text = "Блок с заголовком и контентом (содержит любые внутренние элементы)."


# ------------------------------------------
# Страницы сайта
# ------------------------------------------

class ProgramsPage(Page):
    intro = RichTextField(
        blank=True,
        features=['bold', 'italic'],
        verbose_name="Введение",
        help_text="Краткое описание страницы программ."
    )

    content_panels = Page.content_panels + [FieldPanel('intro')]
    subpage_types = ['programms.CategoryPage']

    class Meta:
        verbose_name = "Программы"
        verbose_name_plural = "Программы"


class CategoryPage(Page):
    description = RichTextField(
        blank=True,
        verbose_name="Описание",
        help_text="Описание категории программ."
    )

    content_panels = Page.content_panels + [FieldPanel('description')]
    parent_page_types = ['programms.ProgramsPage']
    subpage_types = ['programms.ProductPage']

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class ProductPage(Page):
    price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
        verbose_name="Цена",
        help_text="Цена продукта в рублях."
    )

    description = RichTextField(
        blank=True,
        features=['bold', 'italic', 'ol', 'ul', 'link'],
        verbose_name="Описание",
        help_text="Подробное описание продукта."
    )

    buy_link = models.URLField(
        blank=True,
        verbose_name="Ссылка на покупку",
        help_text="URL для покупки продукта."
    )

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Фоновое изображение",
        help_text="Фоновое изображение для hero-секции."
    )

    content = StreamField(
        [
            ('section', SectionBlock()),  # 💡 Новый универсальный блок-секция
        ],
        blank=True,
        null=True,
        verbose_name="Содержимое",
        help_text="Гибкое содержимое страницы с секциями."
    )

    content_panels = Page.content_panels + [
        FieldPanel('price', heading="Цена"),
        FieldPanel('description', heading="Описание"),
        FieldPanel('buy_link', heading="Ссылка на покупку"),
        FieldPanel('hero_image', heading="Фоновое изображение"),
        FieldPanel('content', heading="Содержимое"),
    ]

    parent_page_types = ['programms.CategoryPage']
    subpage_types = []

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
