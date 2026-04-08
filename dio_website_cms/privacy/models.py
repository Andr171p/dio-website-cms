from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class PrivacyPage(Page):
    """Страница политики конфиденциальности"""

    body = RichTextField(blank=True, verbose_name="Содержимое страницы")

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Политика конфиденциальности"
        verbose_name_plural = "Политики конфиденциальности"
