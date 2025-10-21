from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import CharBlock, TextBlock, StructBlock, StreamBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from django.core.paginator import Paginator

# Блок для гибкого контента
class FeatureBlock(StructBlock):
    title = CharBlock(label="Заголовок раздела", required=False)
    description = TextBlock(label="Описание", required=False)
    image = ImageChooserBlock(label="Изображение", required=False)
    document = DocumentChooserBlock(label="Документ", required=False)

    class Meta:
        template = "blocks/feature_block.html"

class ContentStreamBlock(StreamBlock):
    paragraph = TextBlock(label="Параграф")
    feature = FeatureBlock(label="Особенность")

# Категория программ
class ProgramCategoryPage(Page):
    template = "programs/program_category_page.html"
    
    intro = RichTextField(blank=True, features=['bold', 'italic', 'link'], verbose_name="Введение")
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Изображение категории"
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('image'),
    ]

    subpage_types = ['programs.SubCategoryPage', 'programs.ProductPage']
    parent_page_types = ['home.HomePage']

    class Meta:
        verbose_name = "Категория программ"
        verbose_name_plural = "Категории программ"

    def get_context(self, request):
        context = super().get_context(request)
        context['subcategories'] = SubCategoryPage.objects.child_of(self).live()
        return context

# Подкатегория
class SubCategoryPage(Page):
    template = "programs/sub_category_page.html"
    
    intro = RichTextField(blank=True, features=['bold', 'italic', 'link'], verbose_name="Введение")
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Изображение подкатегории"
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('image'),
    ]

    parent_page_types = ['programs.ProgramCategoryPage']
    subpage_types = ['programs.ProductPage']

    class Meta:
        verbose_name = "Подкатегория программ"
        verbose_name_plural = "Подкатегории программ"

    def get_context(self, request):
        context = super().get_context(request)
        products = ProductPage.objects.child_of(self).live()
        
        # Фильтрация по производителю
        manufacturer = request.GET.get('manufacturer')
        if manufacturer and manufacturer != 'all':
            products = products.filter(manufacturer=manufacturer)
        
        # Поиск
        query = request.GET.get('q', '')
        if query:
            products = products.filter(models.Q(title__icontains=query) | models.Q(description__icontains=query))
        
        # Пагинация
        paginator = Paginator(products, 9)  # 9 продуктов на страницу
        page_number = request.GET.get('page')
        products_page = paginator.get_page(page_number)
        
        context['products'] = products_page
        context['manufacturers'] = ProductPage.objects.child_of(self).live().values('manufacturer').distinct()
        context['current_manufacturer'] = manufacturer
        context['search_query'] = query
        return context

# Продукт
class ProductPage(Page):
    template = "programs/product_page.html"
    
    description = RichTextField(blank=True, features=['bold', 'italic', 'link', 'ol', 'ul'], verbose_name="Краткое описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Цена")
    currency = models.CharField(max_length=10, default="₽", verbose_name="Валюта")
    buy_link = models.URLField(blank=True, verbose_name="Ссылка на покупку")
    manufacturer = models.CharField(max_length=100, blank=True, verbose_name="Производитель")
    detailed_content = StreamField([
        ('content', ContentStreamBlock()),
    ], use_json_field=True, blank=True, verbose_name="Детальное содержание")
    features = StreamField([
        ('feature', FeatureBlock()),
    ], use_json_field=True, blank=True, verbose_name="Особенности")
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Изображение продукта"
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('description'),
            FieldPanel('price'),
            FieldPanel('currency'),
            FieldPanel('buy_link'),
            FieldPanel('manufacturer'),
            FieldPanel('image'),
        ], heading="Основная информация"),
        FieldPanel('detailed_content'),
        FieldPanel('features'),
    ]

    parent_page_types = ['programs.ProgramCategoryPage', 'programs.SubCategoryPage']
    subpage_types = []

    def get_context(self, request):
        context = super().get_context(request)
        context['other_products'] = self.get_parent().get_children().live().exclude(pk=self.pk)
        return context

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"