# site_config/models.py
from django.db import models
from wagtail.models import TranslatableMixin
from wagtail.admin.panels import FieldPanel  # Убрали ImageChooserPanel
from wagtail.snippets.models import register_snippet

@register_snippet
class SiteSettings(TranslatableMixin):
    site_title = models.CharField(max_length=255, default="Мой сайт")
    site_description = models.TextField(blank=True)
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    panels = [
        FieldPanel('site_title'),  # Используем FieldPanel вместо ImageChooserPanel
        FieldPanel('site_description'),
        FieldPanel('logo'),  # FieldPanel автоматически определяет тип поля
    ]
    
    def __str__(self):
        return "Настройки сайта"