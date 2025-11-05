from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.utils import timezone
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.search import index
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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

# === НОВЫЕ БЛОКИ ===
class ChallengeBlock(blocks.StructBlock):
    problem = blocks.RichTextBlock(label="Проблема", features=['bold', 'italic'])
    context = blocks.RichTextBlock(label="Контекст (необязательно)", features=['bold', 'italic', 'link'], required=False)

    class Meta:
        template = 'blocks/challenge.html'
        icon = 'warning'
        label = 'Задача (с выделением)'

class SolutionStepBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Название шага")
    description = blocks.RichTextBlock(label="Описание", features=['bold', 'italic', 'link'])
    icon = blocks.ChoiceBlock(
        choices=[
            ('gear', 'Настройка'),
            ('code', 'Разработка'),
            ('database', 'Интеграция'),
            ('eye', 'Визуализация'),
            ('check', 'Тестирование'),
            ('rocket', 'Запуск'),
        ],
        label="Иконка",
        required=False,
        default='gear'
    )

    class Meta:
        icon = 'cogs'

class ResultCardBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Заголовок")
    description = blocks.TextBlock(label="Описание")
    icon = blocks.ChoiceBlock(
        choices=[
            ('zap', 'Скорость'),
            ('link', 'Интеграция'),
            ('eye', 'Визуализация'),
            ('shield', 'Безопасность'),
            ('chart', 'Аналитика'),
            ('check', 'Надёжность'),
        ],
        default='check',
        required=False
    )

    class Meta:
        icon = 'success'

# === ОСНОВНАЯ МОДЕЛЬ ===
class CaseStudyPage(Page):
    customer_name = models.CharField("Название компании-клиента", max_length=255)
    industry = models.CharField("Отрасль", max_length=100, choices=INDUSTRY_CHOICES)
    project_date = models.DateField("Дата реализации проекта", default=timezone.now)
    duration = models.CharField("Длительность проекта", max_length=50, blank=True)
    location = models.CharField("Местоположение", max_length=100, blank=True)

    customer_logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True, blank=True, on_delete=models.SET_NULL, related_name="+",
        verbose_name="Логотип клиента",
    )
    intro = RichTextField("Краткое описание", blank=True)
    main_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True, blank=True, on_delete=models.SET_NULL, related_name="+",
        verbose_name="Основное изображение",
    )

    # === УЛУЧШЕННЫЙ StreamField ===
    content = StreamField([
        ('description', blocks.RichTextBlock(
            label="Описание проекта",
            features=['h2', 'h3', 'bold', 'italic', 'link', 'ol', 'ul']
        )),
        ('challenge', ChallengeBlock()),
        ('solution', blocks.ListBlock(SolutionStepBlock(), label="Шаги решения")),
        ('results', blocks.ListBlock(ResultCardBlock(), label="Результаты (карточки)")),
        ('technologies', blocks.ListBlock(
            blocks.CharBlock(label="Технология"),
            label="Технологии"
        )),
        ('metrics', blocks.ListBlock(
            blocks.StructBlock([
                ('value', blocks.CharBlock(label="Значение")),
                ('description', blocks.CharBlock(label="Описание"))
            ]),
            label="Ключевые метрики"
        )),
    ], blank=True, use_json_field=True, verbose_name="Содержание кейса")

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("customer_name"),
                FieldPanel("industry"),
                FieldPanel("project_date"),
                FieldPanel("duration"),
                FieldPanel("location"),
                FieldPanel("customer_logo"),
                FieldPanel("main_image"),
            ],
            heading="Основная информация",
        ),
        FieldPanel("intro"),
        FieldPanel("content"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("customer_name"),
        index.SearchField("intro"),
    ]

    parent_page_types = ['cases.CaseStudyIndexPage']
    subpage_types = []
    template = "cases/case_study_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        context['other_cases'] = CaseStudyPage.objects.live().exclude(id=self.id).order_by('-project_date')[:3]
        return context

    class Meta:
        verbose_name = "Кейс"
        verbose_name_plural = "Кейсы"


# @ai_indexable(
#     AIPanel("into"),
# )
class CaseStudyIndexPage(Page):
    """Главная страница кейсов"""

    intro = RichTextField("Введение", features=[ "italic", "link"], blank=True)
    items_per_page = models.PositiveIntegerField("Кейсов на странице", default=9)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("items_per_page"),
    ]

    subpage_types = ['cases.CaseStudyPage']
    parent_page_types = ['home.HomePage']

    def get_context(self, request):
        context = super().get_context(request)
        cases = CaseStudyPage.objects.live().order_by("-project_date")

        # Фильтрация по отрасли
        industry = request.GET.get("industry")
        if industry:
            cases = cases.filter(industry=industry)
        context["current_industry"] = industry

        # Пагинация
        paginator = Paginator(cases, self.items_per_page)
        page = request.GET.get("page")
        try:
            cases = paginator.page(page)
        except PageNotAnInteger:
            cases = paginator.page(1)
        except EmptyPage:
            cases = paginator.page(paginator.num_pages)

        context["cases"] = cases
        context["INDUSTRY_CHOICES"] = INDUSTRY_CHOICES
        return context

    template = "cases/case_study_index_page.html"

    class Meta:
        verbose_name = "Лента кейсов"
        verbose_name_plural = "Лента кейсов"