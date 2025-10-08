from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.api.fields import ImageRenditionField as ImageAPIField
from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


# Create your models here.

class ContactPage(Page):
    """Страница контактов"""

    # Поля для контактов
    address = models.TextField(blank=True, verbose_name="Адрес")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Электронная почта")
    map_info = models.TextField(blank=True, verbose_name="Инструкции для карты (например, Embed-код)")
    contact_form_text = models.TextField(blank=True, verbose_name="Текст для формы")
    legal_name = models.CharField(max_length=200, blank=True, verbose_name="Юридическое название")
    inn = models.CharField(max_length=12, blank=True, verbose_name="ИНН")
    ogrn = models.CharField(max_length=13, blank=True, verbose_name="ОГРН")

    # Панели для админки
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("address"),
            FieldPanel("phone"),
            FieldPanel("email"),
        ], heading="Контактная информация"),
        FieldPanel("map_info"),
        FieldPanel("contact_form_text"),
        MultiFieldPanel([
            FieldPanel("legal_name"),
            FieldPanel("inn"),
            FieldPanel("ogrn"),
        ], heading="Юридические данные"),
    ]

    # Указываем шаблон
    template = "contact/contact_page.html"
    class Meta:
        verbose_name = "Страница 'Контакты компании'"
        verbose_name_plural = "Страницы 'Контакты компании'"



