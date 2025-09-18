from typing import ClassVar
from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.images.models import Image
from wagtail.blocks import CharBlock, RichTextBlock, StructBlock, IntegerBlock, BooleanBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks
from news.models import NewsBlock
from .blocks import ContactsBlock, FeedbackFormBlock

MAX_HEADLINE_LENGTH = 100
MAX_SUBHEADLINE_LENGTH = 250

# Блок для слайдов hero-секции
class HeroSlideBlock(blocks.StructBlock):
    """Блок для слайдов hero-секции"""
    headline = blocks.CharBlock(
        max_length=MAX_HEADLINE_LENGTH,
        required=True,
        label="Заголовок слайда"
    )
    subheadline = blocks.CharBlock(
        max_length=MAX_SUBHEADLINE_LENGTH,
        required=False,
        label="Подзаголовок слайда"
    )
    background_image = ImageChooserBlock(
        required=True,
        label="Фоновое изображение",
        help_text="Рекомендуемый размер: 1920x1080px"
    )
    link = blocks.PageChooserBlock(
        required=False,
        label="Ссылка слайда"
    )

    class Meta:
        icon = 'image'
        label = "Слайд героя"

# Блок для отображения кейсов на главной
class CaseStudyBlock(blocks.StructBlock):
    """Блок для отображения кейсов на главной странице"""
    section_title = blocks.CharBlock(
        required=True,
        label="Заголовок секции",
        default="Кейсы и проекты"
    )
    section_description = blocks.TextBlock(
        required=False,
        label="Описание секции",
        default="Более 500 успешно реализованных проектов автоматизации для предприятий различных отраслей и масштабов."
    )
    cases = blocks.ListBlock(
        blocks.PageChooserBlock(
            page_type="cases.CaseStudyPage",
            label="Кейс"
        ),
        label="Выберите кейсы для отображения",
        min_num=3,
        max_num=12
    )
    show_filters = blocks.BooleanBlock(
        default=True,
        required=False,
        label="Показывать фильтры по отраслям"
    )
    show_view_all_button = blocks.BooleanBlock(
        default=True,
        required=False,
        label="Показывать кнопку 'Все кейсы'"
    )

    class Meta:
        icon = 'doc-full'
        label = "Секция кейсов"

# Блок для основного достижения
class MainAchievementBlock(blocks.StructBlock):
    """Блок для основного достижения"""
    icon = ImageChooserBlock(
        required=False,
        label="Иконка",
        help_text="Выберите изображение для иконки (рекомендуемый размер: 50x50px)"
    )
    value = blocks.IntegerBlock(
        default=0,
        label="Числовое значение"
    )
    suffix = blocks.CharBlock(
        max_length=10,
        blank=True,
        default="+",
        label="Суффикс (например, '+' или '%')"
    )
    label = blocks.CharBlock(
        max_length=100,
        label="Краткое название"
    )
    description = blocks.RichTextBlock(
        blank=True,
        label="Описание достижения"
    )

    class Meta:
        icon = 'tick'
        label = "Основное достижение"

# Блок для дополнительного достижения
class AdditionalAchievementBlock(blocks.StructBlock):
    """Блок для дополнительного достижения"""
    value = blocks.CharBlock(
        max_length=10,
        blank=True,
        label="Числовое значение или текст"
    )
    title = blocks.CharBlock(
        max_length=100,
        blank=True,
        label="Заголовок достижения"
    )
    description = blocks.RichTextBlock(
        blank=True,
        label="Описание достижения"
    )

    class Meta:
        icon = 'plus'
        label = "Дополнительное достижение"

# Новый блок для партнёров
class PartnerBlock(blocks.StructBlock):
    """Блок для отображения партнёров"""
    name = blocks.CharBlock(
        max_length=100,
        required=True,
        label="Название партнёра"
    )
    logo = ImageChooserBlock(
        required=True,
        label="Логотип партнёра",
        help_text="Рекомендуемый размер: 200x200px"
    )
    status = blocks.CharBlock(
        max_length=100,
        required=True,
        label="Статус партнёра"
    )
    description = blocks.RichTextBlock(
        required=True,
        label="Описание партнёра"
    )

    class Meta:
        icon = 'group'
        label = "Партнёр"

# Новый блок для сертификатов
class CertificateBlock(blocks.StructBlock):
    """Блок для отображения сертификатов"""
    title = blocks.CharBlock(
        max_length=200,
        required=True,
        label="Название сертификата"
    )

    class Meta:
        icon = 'award'
        label = "Сертификат"

# Новый блок для достижений
class AchievementBlock(blocks.StructBlock):
    """Блок для отображения наград и достижений"""
    title = blocks.CharBlock(
        max_length=100,
        required=True,
        label="Название достижения"
    )
    description = blocks.RichTextBlock(
        required=True,
        label="Описание достижения"
    )

    class Meta:
        icon = 'star'
        label = "Достижение"

# Обновлённая HomePage
class HomePage(Page):
    """Лендинг сайта, главная страница с каруселью"""
    hero_slides = StreamField([
        ("slide", HeroSlideBlock(label="Слайд"))
    ], blank=True, use_json_field=True, verbose_name="Слайды героя")
    case_study_section = StreamField([
        ("case_study", CaseStudyBlock())
    ], blank=True, use_json_field=True, verbose_name="Секция кейсов")
    achievements = StreamField([
        ("main_achievement", MainAchievementBlock()),
        ("additional_achievement", AdditionalAchievementBlock())
    ], blank=True, use_json_field=True, verbose_name="Достижения")
    partners = StreamField([
        ("partner", PartnerBlock())
    ], blank=True, use_json_field=True, verbose_name="Партнёры")
    certificates = StreamField([
        ("certificate", CertificateBlock())
    ], blank=True, use_json_field=True, verbose_name="Сертификаты")
    awards = StreamField([
        ("achievement", AchievementBlock())
    ], blank=True, use_json_field=True, verbose_name="Награды и достижения")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("hero_slides"),
        ], heading="Главная карусель"),
        MultiFieldPanel([
            FieldPanel("case_study_section"),
        ], heading="Секция кейсов"),
        MultiFieldPanel([
            FieldPanel("achievements"),
        ], heading="Достижения"),
        MultiFieldPanel([
            FieldPanel("partners"),
        ], heading="Партнёры"),
        MultiFieldPanel([
            FieldPanel("certificates"),
        ], heading="Сертификаты"),
        MultiFieldPanel([
            FieldPanel("awards"),
        ], heading="Награды и достижения"),
    ]

    api_fields = [
        APIField("hero_slides"),
        APIField("case_study_section"),
        APIField("achievements"),
        APIField("partners"),
        APIField("certificates"),
        APIField("awards"),
    ]

    def get_cases(self, count=6):
        """Получить последние кейсы"""
        from cases.models import CaseStudyPage
        return CaseStudyPage.objects.live().order_by('-project_date')[:count]

    def get_context(self, request, *args, **kwargs):
        from cases.models import CaseStudyPage
        
        # Получаем последние опубликованные кейсы
        context = super().get_context(request, *args, **kwargs)
        context['cases'] = self.get_cases()

        # Получаем все отрасли для фильтров
        try:
            from cases.models import INDUSTRY_CHOICES
            context['INDUSTRY_CHOICES'] = INDUSTRY_CHOICES
        except (ImportError, Exception):
            context['INDUSTRY_CHOICES'] = []

        # Разделяем достижения для отображения
        context["main_achievements"] = [block for block in self.achievements if block.block_type == "main_achievement"]
        context["additional_achievements"] = [block for block in self.achievements if block.block_type == "additional_achievement"]

        # Добавляем данные из новых блоков
        context["partners"] = self.partners
        context["certificates"] = self.certificates
        context["awards"] = self.awards

        return context

    def get_news(self, count=3):
        """Получить последние новости"""
        from news.models import NewsPage
        return NewsPage.objects.live().order_by('-date')[:count]
    
    def get_news_index(self):
        """Получить индексную страницу новостей"""
        from news.models import NewsIndexPage
        return NewsIndexPage.objects.live().first()
    
    def get_children_of_type(self, model_class):
        """Получить дочерние страницы определенного типа"""
        return self.get_children().type(model_class).live()

    class Meta:
        verbose_name = "Главная страница"
        verbose_name_plural = "Главные страницы"