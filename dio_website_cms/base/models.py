from typing import ClassVar

from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import StreamField
from wagtail.snippets.models import register_snippet


@register_setting
class SiteSettings(BaseSiteSetting):
    """Настройки сайта"""
    icon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Логотип компании",
    )


@register_snippet
class NavigationMenu(models.Model):
    """Навигационное меню"""
    title = models.CharField(max_length=100)
    menu_items = StreamField([
        ("page_link", blocks.PageChooserBlock()),
        ("external_link", blocks.StructBlock([
            ("title", blocks.CharBlock(required=True)),
            ("url", blocks.URLBlock(required=True))
        ])),
        ("dropdown", blocks.StructBlock([
            ("title", blocks.CharBlock(required=True)),
            ("submenu_items", blocks.StreamBlock([
                ("page_link", blocks.PageChooserBlock()),
                ("external_link", blocks.StructBlock([
                    ("title", blocks.CharBlock(required=True)),
                    ("url", blocks.URLBlock(required=True))
                ]))
            ]))
        ]))
    ], use_json_field=True, blank=True)
    # Поля для отображения в админ панели
    panels: ClassVar[list[FieldPanel]] = [
        FieldPanel("title"),
        FieldPanel("menu_items"),
    ]

    def __str__(self) -> str:
        return str(self.title)

    class Meta:
        verbose_name = "Навигационное меню"
        verbose_name_plural = "Навигационные меню"
