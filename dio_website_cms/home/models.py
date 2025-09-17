from typing import ClassVar
from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.images.models import Image
from wagtail.blocks import CharBlock, RichTextBlock, StructBlock
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

# Обновлённая HomePage
class HomePage(Page):
    """Лендинг сайта, главная страница с каруселью"""
    hero_slides = StreamField([
        ("slide", HeroSlideBlock(label="Слайд"))
    ], blank=True, use_json_field=True, verbose_name="Слайды героя")

    

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("hero_slides"),
        ], heading="Главная карусель"),
        FieldPanel("achievements"),  # Добавляем панель для редактирования достижений
    ]
    achievements = StreamField([
        ("main_achievement", MainAchievementBlock()),
        ("additional_achievement", AdditionalAchievementBlock())
    ], blank=True, use_json_field=True, verbose_name="Достижения")

    api_fields = [
        APIField("hero_slides"),
        APIField("content_blocks"),
        APIField("achievements"),
    ]

    def get_context(self, request, *args, **kwargs):
        from cases.models import CaseStudyPage
        
        # Получаем последние опубликованные кейсы
        context = super().get_context(request, *args, **kwargs)
        context['latest_cases'] = CaseStudyPage.objects.live().public().order_by('-first_published_at')[:3]

        context["main_achievements"] = [block for block in self.achievements if block.block_type == "main_achievement"]
        context["additional_achievements"] = [block for block in self.achievements if block.block_type == "additional_achievement"]
        # Получаем все отрасли для фильтров
        from cases.models import CaseStudyPage
        industries = CaseStudyPage.objects.live().values_list('industry', flat=True).distinct()
        context['all_industries'] = [industry for industry in industries if industry]
        return context

    def get_news(self, count=3):
        """Получить последние новости"""
        from news.models import NewsPage  # Импорт здесь чтобы избежать циклических импортов
        return NewsPage.objects.live().order_by('-date')[:count]
    def get_cases(self, count=3):
        """Получить последние новости"""
        from cases.models import CaseStudyPage  # Импорт здесь чтобы избежать циклических импортов
        return CaseStudyPage.objects.live().order_by('-date')[:count]
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