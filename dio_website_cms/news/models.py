from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail import blocks
from wagtail.search import index
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class NewsPage(Page):
    """Страница отдельной новости"""
    
    date = models.DateField("Дата публикации", default=timezone.now)
    read_time = models.PositiveSmallIntegerField("Время чтения (мин)", default=3)
    excerpt = models.CharField("Краткое описание", max_length=200)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Изображение"
    )
    content = RichTextField("Содержание")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('read_time'),
            FieldPanel('excerpt'),
            FieldPanel('image'),
        ], heading="Основная информация"),
        FieldPanel('content'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('excerpt'),
        index.SearchField('content'),
    ]

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class NewsIndexPage(Page):
    """Главная страница новостей"""
    intro = RichTextField("Введение", features=['bold', 'italic', 'link'], blank=True)
    items_per_page = models.PositiveIntegerField("Новостей на странице", default=9)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('items_per_page'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        news = NewsPage.objects.live().order_by('-date')
        
        # Пагинация
        paginator = Paginator(news, self.items_per_page)
        page = request.GET.get('page')
        
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
            
        context['news'] = news
        return context

    class Meta:
        verbose_name = "Лента новостей"
        verbose_name_plural = "Ленты новостей"


# Блок для отображения новостей на главной
class NewsBlock(blocks.StructBlock):
    """Блок для отображения новостей на главной странице"""
    title = blocks.CharBlock(
        max_length=100,
        required=True,
        label="Заголовок секции новостей"
    )
    show_count = blocks.IntegerBlock(
        default=3,
        min_value=1,
        max_value=12,
        label="Количество новостей для показа"
    )

    class Meta:
        icon = 'doc-full'
        label = "Блок новостей"