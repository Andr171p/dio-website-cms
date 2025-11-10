from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock


class CertificateBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=200, label="Название сертификата")
    issuer = blocks.CharBlock(max_length=200, label="Кем выдан")
    issue_date = blocks.DateBlock(label="Дата выдачи")
    expiry_date = blocks.DateBlock(required=False, label="Действует до")
    badge_text = blocks.CharBlock(max_length=50, required=False, label="Текст бейджа (например: ISO, Gold Partner)")
    badge_color = blocks.ChoiceBlock(
        choices=[
            ('rose', 'Розовый'),
            ('emerald', 'Зелёный'),
            ('violet', 'Фиолетовый'),
            ('amber', 'Жёлтый'),
            ('blue', 'Синий'),
        ],
        default='rose',
        label="Цвет бейджа"
    )
    thumbnail = ImageChooserBlock(required=False, label="Превью (рекомендуется 600×800)")
    document = DocumentChooserBlock(required=False, label="PDF сертификата")

    class Meta:
        icon = 'certificate'
        label = "Сертификат"


class CertificatesIndexPage(Page):
    intro = models.TextField(blank=True, verbose_name="Вступительный текст")

    body = StreamField([
        ('certificate', CertificateBlock()),
    ], use_json_field=True, collapsed=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    subpage_types = []
    parent_page_types = ['home.HomePage']  # или где хочешь

    def get_context(self, request):
        context = super().get_context(request)
        certificates = [block.value for block in self.body if block.block_type == 'certificate']
        
        # Сортировка по дате (новые сверху)
        certificates.sort(key=lambda x: x['issue_date'], reverse=True)

        # Фильтр по году
        year = request.GET.get('year')
        if year:
            certificates = [c for c in certificates if c['issue_date'].year == int(year)]

        # Фильтр по цвету бейджа (как "тип")
        badge = request.GET.get('badge')
        if badge:
            certificates = [c for c in certificates if c.get('badge_color') == badge]

        # Пагинация
        from django.core.paginator import Paginator
        paginator = Paginator(certificates, 12)
        page = request.GET.get('page')
        context['certificates'] = paginator.get_page(page)

        # Для фильтров
        context['years'] = sorted({c['issue_date'].year for c in [b.value for b in self.body]}, reverse=True)
        context['badge_colors'] = [
            ('rose', 'Розовые'), ('emerald', 'Зелёные'), ('violet', 'Фиолетовые'),
            ('amber', 'Жёлтые'), ('blue', 'Синие')
        ]
        context['current_year'] = year
        context['current_badge'] = badge

        return context