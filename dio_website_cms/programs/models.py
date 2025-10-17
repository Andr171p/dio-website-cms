from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.search import index
from django.utils import timezone
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import CharBlock, TextBlock, StructBlock, ListBlock, PageChooserBlock
from wagtail.blocks import (
    CharBlock, RichTextBlock, StructBlock, ListBlock, PageChooserBlock, ChoiceBlock
)
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Константы для производителей
MANUFACTURER_CHOICES = [
    ("1c-bitrix", "1С-Битрикс"),
    ("abbyy", "ABBYY"),
    ("drweb", "DrWeb"),
    ("entensys", "Entensys"),
    ("eset", "Eset"),
    ("ideco", "Ideco"),
    ("microsoft", "Microsoft"),
    ("navitel", "Navitel"),
    ("nanocad", "nanoCAD"),
    ("norton", "Norton"),
    ("novell", "Novell"),
    ("magix", "Magix"),
    ("panda", "Panda"),
    ("pervasive", "Pervasive"),
    ("pinnacle", "Pinnacle"),
    ("symantec", "Symantec"),
    ("redhat", "RedHat"),
    ("aladdin", "Аладдин Р.Д."),
    ("askon", "АСКОН"),
    ("venta", "Вента"),
    ("vinsmeta", "ВинСмета"),
    ("inek", "ИНЭК"),
    ("kaspersky", "Лаборатория Касперского"),
    ("promt", "ПРОМТ"),
    ("smart-soft", "Смарт-Софт"),
    ("trafika", "Трафика"),
    ("khronobus", "Хронобус"),
    ("ergosolo", "Эргосоло"),
]

# Переиспользуемые блоки из предыдущего ответа
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
    grid_type = blocks.ChoiceBlock(choices=[
        ('numbered', 'Нумерованный'),
        ('bulleted', 'Маркированный'),
        ('icon_grid', 'Сетка с иконками'),
        ('image_grid', 'Сетка с изображениями'),
    ], default='icon_grid', label="Тип сетки")
    items = ListBlock(CardItemBlock(), label="Элементы сетки")

    class Meta:
        icon = "folder-open"
        label = "Универсальная сетка карточек"

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

# Индексная страница "Программы"
class ProgramsIndexPage(Page):
    intro = RichTextField(
        "Введение",
        features=["bold", "italic", "link"],
        blank=True,
        help_text="Краткое описание страницы 'Программы'",
    )
    featured_manufacturers = StreamField([
        ('manufacturer', StructBlock([
            ('name', CharBlock(label="Название производителя")),
            ('description', TextBlock(label="Краткое описание")),
            ('image', ImageChooserBlock(label="Логотип")),
            ('link', PageChooserBlock(label="Ссылка на категорию продуктов", required=False)),
        ]))
    ], blank=True, use_json_field=True, verbose_name="Выделенные производители")

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("featured_manufacturers"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        categories = ProgramCategoryPage.objects.live().child_of(self).order_by("title")
        context["categories"] = categories
        context["featured_manufacturers"] = self.featured_manufacturers
        return context

    class Meta:
        verbose_name = "Индексная страница программ"
        verbose_name_plural = "Индексные страницы программ"

# Категория программ (например, "Панель телефонии для 1C")
class ProgramCategoryPage(Page):
    intro = RichTextField(
        "Введение в категорию",
        features=["bold", "italic", "link"],
        blank=True,
        help_text="Краткое описание категории",
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Изображение категории",
    )
    items_per_page = models.PositiveIntegerField("Продуктов на странице", default=9)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("image"),
        FieldPanel("items_per_page"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        products = SingleProgramPage.objects.live().child_of(self).order_by("-date")
        manufacturer = request.GET.get("manufacturer")
        if manufacturer:
            products = products.filter(manufacturer=manufacturer)
        context["current_manufacturer"] = manufacturer
        context["manufacturer_choices"] = MANUFACTURER_CHOICES

        paginator = Paginator(products, self.items_per_page)
        page = request.GET.get("page")
        try:
            products = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            products = paginator.page(1)

        context["products"] = products
        return context

    class Meta:
        verbose_name = "Категория программ"
        verbose_name_plural = "Категории программ"

# Индивидуальный продукт
class SingleProgramPage(Page):
    date = models.DateField("Дата публикации", default=timezone.now)
    manufacturer = models.CharField(
        max_length=100,
        choices=MANUFACTURER_CHOICES,
        verbose_name="Производитель",
    )
    headline = models.CharField("Заголовок продукта", max_length=255)
    intro = models.TextField("Краткое описание", blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Изображение продукта",
    )
    content = StreamField([
        ('hero', HeroBlock()),
        ('text', TextBlock()),
        ('card_grid', CardGridBlock()),
        ('accordion', AccordionBlock()),
        ('cta', CTABlock()),
    ], blank=True, use_json_field=True, verbose_name="Блоки страницы продукта")

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("date"),
                FieldPanel("manufacturer"),
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
        index.SearchField("manufacturer"),
        index.SearchField("content"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["other_products"] = (
            SingleProgramPage.objects.live().exclude(id=self.id).order_by("-date")[:3]
        )
        return context

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"