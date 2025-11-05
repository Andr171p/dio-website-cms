# programms/models.py
from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import (
    CharBlock, RichTextBlock, StructBlock, ListBlock, StreamBlock,
    RawHTMLBlock, ChoiceBlock
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.contrib.table_block.blocks import TableBlock
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.snippets.models import register_snippet
from modelcluster.models import ClusterableModel


# ========================================
# ДИНАМИЧЕСКИЕ КАТЕГОРИИ (через админку)
# ========================================
@register_snippet
class ProductCategory(ClusterableModel):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория продукта"
        verbose_name_plural = "Категории продуктов"
# ========================================
# БЛОКИ — как в cases
# ========================================
class NumberedListBlock(StructBlock):
    items = ListBlock(RichTextBlock(features=['bold', 'italic']))
    class Meta:
        icon = "list-ol"
        label = "Нумерованный список"


class BulletListBlock(StructBlock):
    items = ListBlock(RichTextBlock(features=['bold', 'italic']))
    class Meta:
        icon = "list-ul"
        label = "Маркированный список"


class ImageCarouselBlock(ListBlock):
    def __init__(self, **kwargs):
        super().__init__(
            StructBlock([
                ('image', ImageChooserBlock()),
                ('caption', CharBlock(required=False)),
            ]),
            **kwargs
        )


class ImageGridBlock(ListBlock):
    def __init__(self, **kwargs):
        super().__init__(
            StructBlock([
                ('image', ImageChooserBlock()),
                ('caption', CharBlock(required=False)),
            ]),
            **kwargs
        )


class CardsBlock(ListBlock):
    def __init__(self, **kwargs):
        super().__init__(
            StructBlock([
                ('title', CharBlock()),
                ('image', ImageChooserBlock(required=False)),
                ('description', RichTextBlock()),
                ('button_text', CharBlock(required=False)),
                ('button_url', CharBlock(required=False)),
            ]),
            **kwargs
        )


class SectionBlock(StructBlock):
    heading = CharBlock()

    content = StreamBlock([
        ("paragraph", RichTextBlock(features=["bold", "italic", "ol", "ul", "link"])),
        ("image", StructBlock([
            ("image", ImageChooserBlock(required=True)),
            ("image_position", ChoiceBlock(choices=[("left", "Слева"), ("right", "Справа")], default="right")),
            ("text_content", StructBlock([
                ("heading", CharBlock(required=True)),
                ("description", RichTextBlock(required=False)),
                ("button_text", CharBlock(required=False)),
                ("button_url", CharBlock(required=False)),
            ]))
        ])),
        ("image_carousel", ImageCarouselBlock()),
        ("image_grid", ImageGridBlock()),
        ("table", TableBlock()),
        ("numbered_list", NumberedListBlock()),
        ("bullet_list", BulletListBlock()),
        ("quote", StructBlock([
            ("text", RichTextBlock()),
            ("author", CharBlock(required=False)),
        ])),
        ("embed", EmbedBlock()),
        ("raw_html", RawHTMLBlock()),
        ("button", StructBlock([
            ("text", CharBlock()),
            ("url", CharBlock()),
        ])),
        ("accordion", ListBlock(StructBlock([
            ("title", CharBlock()),
            ("content", RichTextBlock()),
        ]))),
        ("tabs", ListBlock(StructBlock([
            ("title", CharBlock()),
            ("content", RichTextBlock()),
        ]))),
        ("call_to_action", StructBlock([
            ("title", CharBlock()),
            ("description", RichTextBlock()),
            ("button_text", CharBlock()),
            ("button_url", CharBlock()),
        ])),
        ("divider", StructBlock([])),
        ("spoiler", StructBlock([
            ("title", CharBlock()),
            ("content", RichTextBlock()),
        ])),
        ("cards", CardsBlock()),
        ("document", DocumentChooserBlock()),
        ("metrics", StructBlock([
            ("items", ListBlock(StructBlock([
                ("icon", ImageChooserBlock(required=False)),
                ("value", CharBlock()),
                ("label", CharBlock()),
            ])))
        ])),
    ], required=False)

    class Meta:
        icon = "placeholder"
        label = "Секция с заголовком"

# ========================================
# СТРАНИЦА-КАТАЛОГ: ProgramsPage
# ========================================
class ProgramsPage(Page):
    intro = RichTextField(blank=True, features=[ 'italic'], verbose_name="Введение")

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    subpage_types = ['programms.ProductPage']
    parent_page_types = ['home.HomePage']

    class Meta:
        verbose_name = "Лента Программ"

    def get_context(self, request):
        context = super().get_context(request)

        products = ProductPage.objects.live().order_by('title')
        category_slug = request.GET.get('category')

        # Фильтр по slug
        if category_slug and category_slug != 'all':
            products = products.filter(category__slug=category_slug)

        # Пагинация
        paginator = Paginator(products, 9)
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        # Все категории
        categories = ProductCategory.objects.all()

        context.update({
            'products': products,
            'categories': categories,
            'selected_category': category_slug or 'all',
        })
        return context


# ========================================
# СТРАНИЦА-ПРОДУКТ: ProductPage
# ========================================
class ProductPage(Page):
    category = models.ForeignKey(
        'programms.ProductCategory',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='products',
        verbose_name="Категория"
    )
    price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    description = RichTextField(blank=True, features=[ 'italic', 'ol', 'ul', 'link'])
    buy_link = models.URLField(blank=True)
    hero_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    content = StreamField([
        ('section', SectionBlock()),
    ], blank=True, null=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('category'),
        FieldPanel('price'),
        FieldPanel('description'),
        FieldPanel('buy_link'),
        FieldPanel('hero_image'),
        FieldPanel('content'),
    ]

    parent_page_types = ['programms.ProgramsPage']
    subpage_types = []

    class Meta:
        verbose_name = "Продукт"