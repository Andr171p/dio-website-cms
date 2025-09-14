from typing import ClassVar

from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.models import Page
from wagtail.snippets.models import register_snippet

from .constants import MAX_CHARS_LENGTH, MAX_CONTACT_LENGTH, MAX_ICON_LENGTH


@register_snippet
class HeaderSettings(ClusterableModel):
    """Настройки шапки сайта"""
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    logo_width = models.PositiveIntegerField(default=150, help_text="Ширина логотипа в пикселях")
    company_name = models.CharField(max_length=100, blank=True)

    panels: ClassVar[list[InlinePanel]] = [
        MultiFieldPanel([
            FieldPanel("logo"),
            FieldPanel("logo_width"),
            FieldPanel("company_name"),
        ], heading="Логотип"),
        InlinePanel("menu_items", label="Пункты меню"),
    ]

    def __str__(self):
        return "Настройки шапки"


class MenuItem(ClusterableModel):
    header = ParentalKey(
        HeaderSettings,
        on_delete=models.CASCADE,
        related_name="menu_items",
    )
    title = models.CharField(max_length=100)
    link_url = models.CharField(max_length=500, blank=True)
    link_page = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.CASCADE,
    )
    has_dropdown = models.BooleanField(default=False, help_text="Есть выпадающее меню")
    sort_order = models.IntegerField(default=0)

    panels: ClassVar[list[FieldPanel | InlinePanel]] = [
        FieldPanel("title"),
        FieldPanel("link_url"),
        FieldPanel("link_page"),
        FieldPanel("has_dropdown"),
        FieldPanel("sort_order"),
        InlinePanel("dropdown_items", label="Элементы выпадающего меню"),
    ]

    class Meta:
        ordering: ClassVar[list[str]] = ["sort_order"]

    @property
    def url(self) -> str:
        if self.link_page:
            return self.link_page.url
        return self.link_url or "#"

    def __str__(self) -> str:
        return str(self.title)


class DropdownItem(models.Model):
    menu_item = ParentalKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name="dropdown_items"
    )
    title = models.CharField(max_length=100)
    link_url = models.CharField(max_length=500, blank=True)
    link_page = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.CASCADE
    )
    sort_order = models.IntegerField(default=0)

    panels: ClassVar[list[FieldPanel]] = [
        FieldPanel("title"),
        FieldPanel("link_url"),
        FieldPanel("link_page"),
        FieldPanel("sort_order"),
    ]

    class Meta:
        ordering: ClassVar[list[str]] = ["sort_order"]

    @property
    def url(self) -> str:
        if self.link_page:
            return self.link_page.url
        return self.link_url or "#"

    def __str__(self) -> str:
        return str(self.title)


@register_snippet
class Contact(models.Model):
    """Контакты компании"""
    CONTACT_TYPE_CHOICES: ClassVar[list[tuple]] = [
        ("phone", "Телефон"),
        ("email", "Email"),
        ("address", "Адрес"),
        ("whatsapp", "Whatsapp"),
        ("telegram", "Telegram"),
        ("other", "Другое"),
    ]

    contact_type = models.CharField(
        max_length=MAX_CONTACT_LENGTH, choices=CONTACT_TYPE_CHOICES, verbose_name="Тип контакта"
    )
    value = models.CharField(max_length=MAX_CHARS_LENGTH, verbose_name="Значение")
    label = models.CharField(
        max_length=MAX_CONTACT_LENGTH,
        blank=True,
        verbose_name="Подпись контакта",
        help_text="Например: 'Основной телефон', 'Электронная почта'"
    )
    icon = models.CharField(
        max_length=MAX_ICON_LENGTH,
        blank=True,
        verbose_name="Иконка",
        help_text="Название иконки (например: 'phone', 'email')"
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name="Основной контакт"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок отображения"
    )

    panels: ClassVar[list[FieldPanel]] = [
        FieldPanel("contact_type"),
        FieldPanel("value"),
        FieldPanel("label"),
        FieldPanel("icon"),
        FieldPanel("is_primary"),
        FieldPanel("order"),
    ]

    def __str__(self) -> str:
        return f"{self.get_contact_type_display()}: {self.value}"

    class Meta:
        verbose_name = "Контакт компании"
        verbose_name_plural = "Контакты компании"
        ordering: ClassVar[list[str]] = ["order", "contact_type"]
