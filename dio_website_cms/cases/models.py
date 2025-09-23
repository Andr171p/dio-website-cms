from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.search import index
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtailai.panels import AIPanel, ai_indexable

# Константы для отраслей
INDUSTRY_CHOICES = [
    ("oil-gas", "Нефтегаз"),
    ("manufacturing", "Производство"),
    ("construction", "Строительство"),
    ("government", "Госсектор"),
    ("retail", "Ритейл"),
    ("logistics", "Логистика"),
    ("finance", "Финансы"),
    ("healthcare", "Здравоохранение"),
]

class CaseStudyPage(Page):
    """Страница отдельного кейса"""
    customer_name = models.CharField("Название компании-клиента", max_length=255)
    industry = models.CharField("Отрасль", max_length=100, choices=INDUSTRY_CHOICES)
    project_date = models.DateField("Дата реализации проекта", default=timezone.now)
    duration = models.CharField("Длительность проекта", max_length=50, blank=True)
    location = models.CharField("Местоположение", max_length=100, blank=True)
    
    customer_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Логотип клиента"
    )
    
    intro = RichTextField("Краткое описание", blank=True, help_text="1-3 предложения для анонса")
    
    # Основное изображение кейса
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Основное изображение"
    )
    
    # Детальное содержание
    content = StreamField([
        ('description', blocks.RichTextBlock(label="Описание проекта")),
        ('challenge', blocks.RichTextBlock(label="Задача")),
        ('solution', blocks.RichTextBlock(label="Решение")),
        ('results', blocks.RichTextBlock(label="Результаты")),
        ('technologies', blocks.ListBlock(
            blocks.CharBlock(label="Технология"),
            label="Используемые технологии"
        )),
        ('metrics', blocks.ListBlock(
            blocks.StructBlock([
                ('value', blocks.CharBlock(label="Значение")),
                ('description', blocks.CharBlock(label="Описание метрики"))
            ]),
            label="Ключевые метрики"
        )),
    ], blank=True, use_json_field=True, verbose_name="Содержание кейса")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('customer_name'),
            FieldPanel('industry'),
            FieldPanel('project_date'),
            FieldPanel('duration'),
            FieldPanel('location'),
            FieldPanel('customer_logo'),
            FieldPanel('main_image'),
        ], heading="Основная информация"),
        FieldPanel('intro'),
        FieldPanel('content'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('customer_name'),
        index.SearchField('intro'),
        index.SearchField('content'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        # Другие кейсы (исключая текущую)
        context['other_cases'] = CaseStudyPage.objects.live().exclude(id=self.id).order_by('-project_date')[:3]
        return context

    template = "cases/case_study_page.html"
    
    class Meta:
        verbose_name = "Кейс"
        verbose_name_plural = "Кейсы"

@ai_indexable(
    AIPanel("into"),
)
class CaseStudyIndexPage(Page):
    """Главная страница кейсов"""
    intro = RichTextField("Введение", features=['bold', 'italic', 'link'], blank=True)
    items_per_page = models.PositiveIntegerField("Кейсов на странице", default=9)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('items_per_page'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        cases = CaseStudyPage.objects.live().order_by('-project_date')
        
        # Фильтрация по отрасли
        industry = request.GET.get('industry')
        if industry:
            cases = cases.filter(industry=industry)
        context['current_industry'] = industry

        # Пагинация
        paginator = Paginator(cases, self.items_per_page)
        page = request.GET.get('page')
        try:
            cases = paginator.page(page)
        except PageNotAnInteger:
            cases = paginator.page(1)
        except EmptyPage:
            cases = paginator.page(paginator.num_pages)

        context['cases'] = cases
        context['INDUSTRY_CHOICES'] = INDUSTRY_CHOICES
        return context

    template = "cases/case_study_index_page.html"
    
    class Meta:
        verbose_name = "Портфолио кейсов"
        verbose_name_plural = "Портфолио кейсов"