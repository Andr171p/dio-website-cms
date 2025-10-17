from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.api import APIField
from wagtail.fields import RichTextField
from wagtail.blocks import (
    CharBlock,
    StructBlock,
)
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from services.models import ServiceBlock

from feedback.forms import FeedbackForm


MAX_HEADLINE_LENGTH = 500
MAX_SUBHEADLINE_LENGTH = 250


# Блок для отображения кейсов на главной
class CaseStudyBlock(blocks.StructBlock):
    """Блок для отображения кейсов на главной странице"""

    section_title = blocks.CharBlock(
        required=True, label="Заголовок секции", default="Кейсы и проекты"
    )
    section_description = blocks.TextBlock(
        required=False,
        label="Описание секции",
        default="Более 500 успешно реализованных проектов автоматизации для предприятий различных отраслей и масштабов.",
    )
    cases = blocks.ListBlock(
        blocks.PageChooserBlock(page_type="cases.CaseStudyPage", label="Кейс"),
        label="Выберите кейсы для отображения",
        min_num=3,
        max_num=12,
    )
    show_filters = blocks.BooleanBlock(
        default=True, required=False, label="Показывать фильтры по отраслям"
    )
    show_view_all_button = blocks.BooleanBlock(
        default=True, required=False, label="Показывать кнопку 'Все кейсы'"
    )

    class Meta:
        icon = "doc-full"
        label = "Секция кейсов"


# Блок для основного достижения
class MainAchievementBlock(blocks.StructBlock):
    """Блок для основного достижения"""

    icon = ImageChooserBlock(
        required=False,
        label="Иконка",
        help_text="Выберите изображение для иконки (рекомендуемый размер: 50x50px)",
    )
    value = blocks.IntegerBlock(default=0, label="Числовое значение")
    suffix = blocks.CharBlock(
        max_length=10, blank=True, default="+", label="Суффикс (например, '+' или '%')"
    )
    label = blocks.CharBlock(max_length=100, label="Краткое название")
    description = blocks.RichTextBlock(blank=True, label="Описание достижения")

    class Meta:
        icon = "tick"
        label = "Основное достижение"


# Блок для дополнительного достижения
class AdditionalAchievementBlock(blocks.StructBlock):
    """Блок для дополнительного достижения"""

    value = blocks.CharBlock(
        max_length=10, blank=True, label="Числовое значение или текст"
    )
    title = blocks.CharBlock(max_length=100, blank=True, label="Заголовок достижения")
    description = blocks.RichTextBlock(blank=True, label="Описание достижения")

    class Meta:
        icon = "plus"
        label = "Дополнительное достижение"


# Новый блок для партнёров
class PartnerBlock(blocks.StructBlock):
    """Блок для отображения партнёров"""

    name = blocks.CharBlock(max_length=100, required=True, label="Название партнёра")
    logo = ImageChooserBlock(
        required=True,
        label="Логотип партнёра",
        help_text="Рекомендуемый размер: 200x200px",
    )
    status = blocks.CharBlock(max_length=100, required=True, label="Статус партнёра")
    description = blocks.RichTextBlock(required=True, label="Описание партнёра")

    class Meta:
        icon = "group"
        label = "Партнёр"


# Новый блок для сертификатов
class CertificateBlock(blocks.StructBlock):
    """Блок для отображения сертификатов"""

    title = blocks.CharBlock(
        max_length=200, required=True, label="Название сертификата"
    )

    class Meta:
        icon = "award"
        label = "Сертификат"


# Новый блок для достижений
class AchievementBlock(blocks.StructBlock):
    """Блок для отображения наград и достижений"""

    title = blocks.CharBlock(max_length=100, required=True, label="Название достижения")
    description = blocks.RichTextBlock(required=True, label="Описание достижения")

    class Meta:
        icon = "star"
        label = "Достижение"


# Блок для слайдов hero-секции
class HeroSlideBlock(blocks.StructBlock):
    """Блок для слайдов hero-секции с несколькими изображениями"""

    headline = blocks.CharBlock(
        max_length=MAX_HEADLINE_LENGTH, required=True, label="Заголовок слайда"
    )
    subheadline = blocks.CharBlock(
        max_length=MAX_SUBHEADLINE_LENGTH, required=False, label="Подзаголовок слайда"
    )
    images = blocks.ListBlock(
        ImageChooserBlock(
            required=True,
            label="Изображение",
            help_text="Рекомендуемый размер: 1920x1080px",
        ),
        min_num=1,
        max_num=3,
        label="Изображения слайда (до 3)",
        help_text="Добавьте до 3 изображений для разных видов: фон, команда, индивидуальное использование",
    )
    link = blocks.PageChooserBlock(required=False, label="Ссылка слайда")

    class Meta:
        icon = "image"
        label = "Слайд героя"


# Блок для кнопок
class ButtonBlock(blocks.StructBlock):
    """Блок для кнопок в header"""

    text = blocks.CharBlock(max_length=50, required=True, label="Текст кнопки")
    url = blocks.URLBlock(required=True, label="Ссылка кнопки")
    is_secondary = blocks.BooleanBlock(
        required=False, default=False, label="Вторичная кнопка"
    )

    class Meta:
        icon = "link"
        label = "Кнопка"


# Блок для header-секции
class HeaderBlock(blocks.StructBlock):
    """Блок для hero-секции с каруселью"""

    slides = blocks.StreamBlock(
        [
            ("slide", HeroSlideBlock()),
        ],
        required=True,
        label="Слайды",
    )
    buttons = blocks.ListBlock(ButtonBlock(), required=False, label="Кнопки")

    class Meta:
        icon = "view"
        label = "Header (Hero Section)"


# Блок для логотипов партнёров
class PartnerLogoBlock(blocks.StructBlock):
    """Блок для логотипа партнёра"""

    logo = ImageChooserBlock(
        required=True,
        label="Логотип партнёра",
        help_text="Рекомендуемый размер: 54x16px",
    )
    link = blocks.URLBlock(required=False, label="Ссылка на партнёра")

    class Meta:
        icon = "image"
        label = "Логотип партнёра"


class PartnershipBlock(blocks.StructBlock):
    """Блок для секции с партнёрствами"""

    headline = blocks.CharBlock(
        max_length=MAX_HEADLINE_LENGTH, required=True, label="Заголовок секции"
    )
    subheadline = blocks.CharBlock(
        max_length=MAX_SUBHEADLINE_LENGTH, required=True, label="Подзаголовок секции"
    )
    logos = blocks.ListBlock(
        PartnerLogoBlock(),
        min_num=1,
        max_num=6,
        label="Логотипы партнёров",
        help_text="Добавьте до 6 логотипов",
    )

    class Meta:
        icon = "group"
        label = "Секция партнёрств"

class GlobalPresenceBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
        default="Глобальное присутствие",
        label="Заголовок"
    )
    description = blocks.RichTextBlock(required=False, label="Описание")
    image = ImageChooserBlock(
        required=True,
        label="Изображение для локации",
        help_text="Рекомендуемый размер: квадратное или 1x1"
    )


class HomePage(Page):
    """Лендинг сайта, главная страница с каруселью и header"""
    global_presence = StreamField(
        [
            ('presence', GlobalPresenceBlock())
        ],
        use_json_field=True,
        blank=True,
        max_num=1,  # Только один блок
        verbose_name="Блок 'Глобальное присутствие'"
    )

    header_section = StreamField(
        [("header", HeaderBlock(label="Header секция"))],
        blank=True,
        use_json_field=True,
        verbose_name="Header секция",
    )
    hero_slides = StreamField(
        [("slide", HeroSlideBlock(label="Слайд"))],
        blank=True,
        use_json_field=True,
        verbose_name="Слайды героя",
    )
    case_study_section = StreamField(
        [("case_study", CaseStudyBlock())],
        blank=True,
        use_json_field=True,
        verbose_name="Секция кейсов",
    )
    achievements = StreamField(
        [
            ("main_achievement", MainAchievementBlock()),
            ("additional_achievement", AdditionalAchievementBlock()),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Достижения",
    )
    partners = StreamField(
        [("partner", PartnerBlock())],
        blank=True,
        use_json_field=True,
        verbose_name="Партнёры",
    )
    certificates = StreamField(
        [("certificate", CertificateBlock())],
        blank=True,
        use_json_field=True,
        verbose_name="Сертификаты",
    )
    awards = StreamField(
        [("achievement", AchievementBlock())],
        blank=True,
        use_json_field=True,
        verbose_name="Награды и достижения",
    )
    partnership_section = StreamField(
        [("partnership", PartnershipBlock(label="Секция партнёрств"))],
        blank=True,
        use_json_field=True,
        verbose_name="Секция партнёрств",
    )

    eyebrow = models.CharField(
        max_length=255, blank=True, help_text="Подзаголовок над основным заголовком"
    )
    heading = models.CharField(
        max_length=255, blank=True, help_text="Основной заголовок"
    )
    subheading = models.TextField(blank=True, help_text="Подзаголовок или описание")

    content = StreamField(
        [
            (
                "hero",
                StructBlock(
                    [
                        ("title", CharBlock(required=True, label="Заголовок")),
                        (
                            "image",
                            ImageChooserBlock(required=True, label="Изображение"),
                        ),
                    ]
                ),
            ),
            ("services_section", ServiceBlock()),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Секции страницы",
    )

    content_panels = Page.content_panels + [
         FieldPanel('global_presence'),

        MultiFieldPanel(
            [
                FieldPanel("content"),
            ],
            heading="Секции страницы",
        ),
        MultiFieldPanel(
            [
                FieldPanel("eyebrow"),
                FieldPanel("heading"),
                FieldPanel("subheading"),
            ],
            heading="Заголовок и описание",
        ),
        MultiFieldPanel(
            [
                FieldPanel("header_section"),
            ],
            heading="Главный блок",
        ),
        MultiFieldPanel(
            [
                FieldPanel("achievements"),
            ],
            heading="Достижения",
        ),
        
        MultiFieldPanel(
            [
                FieldPanel("partnership_section"),
            ],
            heading="Секция партнёрств",
        ),
    ]

    api_fields = [
        APIField("header_section"),
        APIField("hero_slides"),
        APIField("case_study_section"),
        APIField("achievements"),
        APIField("partners"),
        APIField("certificates"),
        APIField("awards"),
        APIField("partnership_section"),
        APIField("content_panels"),
        APIField("content"),
    ]

    def get_services(self, count=6):
        """Получить последние услуги из связанной SingleServicePage"""
        from services.models import SingleServicePage

        return SingleServicePage.objects.live().order_by("-date")[:count]

    def get_cases(self, count=6):
        """Получить последние кейсы"""
        from cases.models import CaseStudyPage

        return CaseStudyPage.objects.live().order_by("-project_date")[:count]

    def get_context(self, request, *args, **kwargs):

        context = super().get_context(request, *args, **kwargs)
        context["cases"] = self.get_cases()
        context["form"] = FeedbackForm()
        try:
            from cases.models import INDUSTRY_CHOICES

            context["INDUSTRY_CHOICES"] = INDUSTRY_CHOICES
        except (ImportError, Exception):
            context["INDUSTRY_CHOICES"] = []

        context["main_achievements"] = [
            block
            for block in self.achievements
            if block.block_type == "main_achievement"
        ]
        context["additional_achievements"] = [
            block
            for block in self.achievements
            if block.block_type == "additional_achievement"
        ]

        context["partners"] = self.partners
        context["certificates"] = self.certificates
        context["awards"] = self.awards
        context["partnership_section"] = self.partnership_section

        return context

    def get_news(self, count=3):
        """Получить последние новости"""
        from news.models import NewsPage

        return NewsPage.objects.live().order_by("-date")[:count]

    def get_news_index(self):
        """Получить индексную страницу новостей"""
        from news.models import NewsIndexPage

        return NewsIndexPage.objects.live().first()

    def get_children_of_type(self, model_class):
        """Получить дочерние страницы определенного типа"""
        return self.get_children().type(model_class).live()

    def get_preview_template(self, request, mode_name):
        return "home/home_page.html"

    class Meta:
        verbose_name = "Главная страница"
        verbose_name_plural = "Главные страницы"

