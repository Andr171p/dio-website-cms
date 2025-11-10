# career/models.py
from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index


class CareerPage(Page):
    intro = models.CharField(max_length=255, blank=True, default="Присоединяйся к лидерам")

    content = StreamField([
        ('hero', blocks.StructBlock([
            ('title', blocks.CharBlock(default="Карьера в Дио-Консалт")),
            ('subtitle', blocks.RichTextBlock(required=False)),
            ('background_image', ImageChooserBlock(required=True)),
            ('cta_text', blocks.CharBlock(default="О компании")),
            ('cta_link', blocks.PageChooserBlock(required=False)),
        ], icon="image")),
        ('values', blocks.StructBlock([
            ('title', blocks.CharBlock(default="Наши ценности")),
            ('items', blocks.ListBlock(blocks.StructBlock([
                ('title', blocks.CharBlock()),
                ('description', blocks.RichTextBlock(required=False)),
                ('icon', ImageChooserBlock(required=False)),
            ]))),
        ], icon="list-ul")),
        ('vacancies_list', blocks.StructBlock([
            ('title', blocks.CharBlock(default="Открытые вакансии")),
        ], icon="user")),
        ('form', blocks.StructBlock([
            ('title', blocks.CharBlock(default="Хотите в команду?")),
            ('description', blocks.RichTextBlock(required=False)),
        ], icon="mail")),
        ('office', blocks.StructBlock([
            ('title', blocks.CharBlock(default="Наш офис")),
            ('address', blocks.CharBlock(required=False)),
        ], icon="home")),
    ], blank=True, default=[], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("content"),
    ]

    subpage_types = ['career.CareerVacancyPage']
    parent_page_types = ['home.HomePage']
class CareerVacancyPage(Page):
    # Основные поля (не в StreamField!)
    department = models.CharField(max_length=100, default="Продажи")
    salary = models.CharField(max_length=100, default="от 120 000 ₽")
    experience = models.CharField(max_length=100, blank=True, help_text="Например: от 1 года")
    badge = models.CharField(max_length=20, blank=True, choices=[
        ('hot', 'Горячая'),
        ('new', 'Новинка'),
        ('remote', 'Удалённо'),
        ('urgent', 'Срочно'),
    ], help_text="Метка на карточке")

    background = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )

    # Умный StreamField — только контент!
    body = StreamField([
        ('duties', blocks.StructBlock([
            ('title', blocks.CharBlock(default="Обязанности")),
            ('items', blocks.ListBlock(blocks.TextBlock(icon="arrow-right"))),
        ], icon="list-ul", label="Обязанности")),

        ('requirements', blocks.StructBlock([
            ('title', blocks.CharBlock(default="Требования")),
            ('items', blocks.ListBlock(blocks.TextBlock(icon="user"))),
        ], icon="warning", label="Требования")),

        ('bonus', blocks.StructBlock([
            ('title', blocks.CharBlock(default="Будет плюсом")),
            ('items', blocks.ListBlock(blocks.TextBlock(icon="star"))),
        ], icon="pick", label="Плюсом")),

        ('conditions', blocks.ListBlock(
            blocks.StructBlock([
                ('icon', blocks.ChoiceBlock(choices=[
                    ('briefcase', 'Офис'),
                    ('clock', 'График'),
                    ('rub', 'Зарплата'),
                    ('heart', 'ДМС'),
                    ('dumbbell', 'Спорт'),
                    ('pizza', 'Еда'),
                    ('home', 'Удалённо'),
                    ('gift', 'Бонусы'),
                ], default='briefcase', icon="cog")),
                ('text', blocks.TextBlock()),
            ], icon="cog"),
            label="Условие"
        )),

        ('gallery', blocks.StructBlock([
            ('title', blocks.CharBlock(default="Наш офис — это кайф")),
            ('images', blocks.ListBlock(ImageChooserBlock())),
            ('layout', blocks.ChoiceBlock(choices=[
                ('grid', 'Сетка'),
                ('masonry', 'Кирпичики'),
                ('carousel', 'Карусель'),
            ], default='grid')),
        ], icon="image", label="Галерея")),

        ('video', blocks.URLBlock(help_text="YouTube или Vimeo")),
        
        ('cta', blocks.StructBlock([
            ('text', blocks.CharBlock(default="Готов стать частью команды?")),
            ('button_text', blocks.CharBlock(default="Откликнуться за 30 секунд")),
        ], icon="mail", label="Призыв к действию")),
    ], use_json_field=True, blank=True)

    # Панели — всё по полочкам!
    content_panels = [
        MultiFieldPanel([
            FieldPanel('title', classname="full title"),
            FieldPanel('department'),
            FieldPanel('salary'),
            FieldPanel('experience'),
            FieldPanel('badge'),
            FieldPanel('background'),
        ], heading="Вакансия — основное", classname="collapsible"),

        FieldPanel('body'),
    ]

    promote_panels = Page.promote_panels

    parent_page_types = ['career.CareerPage']
    subpage_types = []

    class Meta:
        verbose_name = "Вакансия"