from typing import Any, ClassVar

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, Panel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField

from .forms import FeedbackForm


@register_setting
class SiteSettings(BaseSiteSetting):
    """Настройки сайта"""
    name = models.CharField(max_length=100, verbose_name="Название компании")
    icon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Логотип компании",
    )
    address = models.TextField()

    panels: ClassVar[list[FieldPanel]] = [
        FieldPanel("name"),
        FieldPanel("icon"),
        FieldPanel("address"),
    ]

    class Meta:
        verbose_name = "Настройки сайта"


@register_setting
class HeaderSettings(BaseSiteSetting):
    """Настройки header сайта"""
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Логотип"
    )
    feedback_button_text = models.CharField(
        max_length=50,
        default="Связаться с нами",
        verbose_name="Текст кнопки"
    )
    feedback_button_url = models.URLField(blank=True, verbose_name="Ссылка кнопки")

    panels: ClassVar[list[FieldPanel]] = [
        FieldPanel("logo"),
        FieldPanel("feedback_button_text"),
        FieldPanel("feedback_button_url"),
    ]

    class Meta:
        verbose_name = "Настройки header"


class FormField(AbstractFormField):
    page = ParentalKey(
        "ContactPage",
        on_delete=models.CASCADE,
        related_name="form_fields"
    )


class ContactPage(AbstractEmailForm):
    intro = RichTextField(blank=True, features=["bold", "link", "ol", "ul"])
    thanks = RichTextField(blank=True, features=["bold", "link"])

    content_panels: ClassVar[list[Panel]] = [
        *AbstractEmailForm.content_panels,
        FieldPanel("intro"),
        InlinePanel("form_fields", label="FormFields"),
        FieldPanel("thanks"),
    ]

    def get_form_class(self) -> type[FeedbackForm]:  # noqa: PLR6301
        return FeedbackForm

    def get_form(self, *args, **kwargs) -> Any:
        return super().get_form(*args, **kwargs)
