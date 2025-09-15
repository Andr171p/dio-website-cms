from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PublishingPanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail import blocks
from wagtail.fields import StreamField
from wagtail.blocks import PageChooserBlock, CharBlock, URLBlock, StructBlock, ListBlock, TextBlock
from wagtail.models import DraftStateMixin, RevisionMixin, PreviewableMixin

# ========== HEADER SETTINGS ==========
@register_setting
class HeaderSettings(DraftStateMixin, RevisionMixin, PreviewableMixin, BaseGenericSetting):
    """Настройки хедера сайта"""
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Логотип сайта",
        help_text="Логотип для header. Рекомендуемый размер: 40x40px"
    )
    site_title = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Название сайта",
        help_text="Название, которое отображается в header"
    )
    site_subtitle = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Подзаголовок сайта",
        help_text="Подзаголовок, отображаемый под названием сайта"
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Телефон",
        help_text="Основной телефон для связи"
    )
    email = models.EmailField(
        blank=True,
        verbose_name="Email",
        help_text="Основной email для связи"
    )
    consultation_button_text = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Текст кнопки консультации",
        help_text="Текст для кнопки консультации",
        default="Консультация"
    )
    
    # Навигационное меню с подменю
    nav_items = StreamField([
        ("nav_item", blocks.StructBlock([
            ("name", blocks.CharBlock(max_length=50, label="Название пункта")),
            ("href", blocks.CharBlock(max_length=100, label="Ссылка (например, /about или #contact)", blank=True)),
            ("page_link", PageChooserBlock(label="Ссылка на страницу Wagtail", required=False)),
            ("submenu", blocks.ListBlock(blocks.StructBlock([
                ("name", blocks.CharBlock(max_length=50, label="Название подпункта")),
                ("href", blocks.CharBlock(max_length=100, label="Ссылка подпункта", blank=True)),
                ("page_link", PageChooserBlock(label="Ссылка на страницу Wagtail", required=False)),
            ]), label="Подменю", blank=True, max_num=5)),
        ], label="Пункт меню"))
    ], blank=True, use_json_field=True, verbose_name="Пункты меню")

    panels = [
        MultiFieldPanel([
            FieldPanel("logo"),
            FieldPanel("site_title"),
            FieldPanel("site_subtitle"),
            FieldPanel("phone_number"),
            FieldPanel("email"),
            FieldPanel("consultation_button_text"),
            FieldPanel("nav_items"),
        ], heading="Основные настройки header"),
        PublishingPanel(),  # Добавляем панель публикации
    ]

    class Meta:
        verbose_name = "Настройки хедера"
        verbose_name_plural = "Настройки хедеров"

    def get_preview_template(self, request, mode_name):
        return "base.html"

    def get_preview_context(self, request, mode_name):
        return {"settings": self}

# ========== FOOTER SETTINGS ==========
# base/models.py или где определена ваша модель



@register_setting
class FooterSettings(DraftStateMixin, RevisionMixin, PreviewableMixin, BaseGenericSetting):
    """Настройки футера сайта"""

    # Основные настройки
    copyright_text = models.CharField(
        max_length=200,
        default="© 2025 Все права защищены",
        verbose_name="Текст копирайта"
    )
    company_address = models.TextField(
        blank=True,
        verbose_name="Адрес компании"
    )
    working_hours = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Часы работы"
    )

    # Социальные сети
    social_links = StreamField([
        ("social", StructBlock([
            ("platform", CharBlock(max_length=50, label="Платформа")),
            ("url", URLBlock(label="Ссылка")),
            ("icon", CharBlock(max_length=50, label="Иконка (например, facebook, twitter)")),
        ], label="Социальная сеть"))
    ], blank=True, use_json_field=True, verbose_name="Социальные сети")

    # Секции футера
    company_links = StreamField([
        ("link", StructBlock([
            ("title", CharBlock(max_length=100, label="Заголовок")),
            ("url", URLBlock(label="Ссылка", required=False)),
            ("anchor", CharBlock(max_length=100, label="Якорь (например, #about)", required=False)),
        ], label="Ссылка компании"))
    ], blank=True, use_json_field=True, verbose_name="Ссылки компании")

    services_links = StreamField([
        ("link", StructBlock([
            ("title", CharBlock(max_length=100, label="Заголовок")),
            ("url", URLBlock(label="Ссылка", required=False)),
            ("anchor", CharBlock(max_length=100, label="Якорь (например, #services)", required=False)),
        ], label="Ссылка услуги"))
    ], blank=True, use_json_field=True, verbose_name="Ссылки услуг")

    industries_links = StreamField([
        ("link", StructBlock([
            ("title", CharBlock(max_length=100, label="Заголовок")),
            ("url", URLBlock(label="Ссылка", required=False)),
            ("anchor", CharBlock(max_length=100, label="Якорь", required=False)),
        ], label="Ссылка отрасли"))
    ], blank=True, use_json_field=True, verbose_name="Ссылки отраслей")

    certifications = StreamField([
        ("cert", StructBlock([
            ("title", CharBlock(max_length=100, label="Название сертификации")),
        ], label="Сертификация"))
    ], blank=True, use_json_field=True, verbose_name="Сертификации")

    # Панели админки
    content_panels = [
        MultiFieldPanel([
            FieldPanel("copyright_text"),
            FieldPanel("company_address"),
            FieldPanel("working_hours"),
            FieldPanel("social_links"),
            FieldPanel("company_links"),
            FieldPanel("services_links"),
            FieldPanel("industries_links"),
            FieldPanel("certifications"),
        ], heading="Настройки футера"),
    ]

    publish_panels = [
        PublishingPanel(),
    ]

    class Meta:
        verbose_name = "Настройки футера"
        verbose_name_plural = "Настройки футеров"

    def get_preview_template(self, request, mode_name):
        return "base.html"

    def get_preview_context(self, request, mode_name):
        return {"settings": self}


# ========== CONTACT SETTINGS ==========
@register_setting
class ContactSettings(DraftStateMixin, RevisionMixin, PreviewableMixin, BaseGenericSetting):
    """Настройки контактов"""
    primary_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Основной телефон"
    )
    secondary_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Дополнительный телефон"
    )
    primary_email = models.EmailField(
        blank=True,
        verbose_name="Основной email"
    )
    secondary_email = models.EmailField(
        blank=True,
        verbose_name="Дополнительный email"
    )
    address = models.TextField(
        blank=True,
        verbose_name="Адрес"
    )
    map_embed_code = models.TextField(
        blank=True,
        verbose_name="Код карты",
        help_text="HTML код для встраивания карты"
    )

    content_panels = [
        MultiFieldPanel([
            FieldPanel("primary_phone"),
            FieldPanel("secondary_phone"),
            FieldPanel("primary_email"),
            FieldPanel("secondary_email"),
            FieldPanel("address"),
            FieldPanel("map_embed_code"),
        ], heading="Контактная информация"),
    ]

    publish_panels = [
        PublishingPanel(),
    ]



    class Meta:
        verbose_name = "Настройки контактов"
        verbose_name_plural = "Настройки контактов"

    def get_preview_template(self, request, mode_name):
        return "base.html"

    def get_preview_context(self, request, mode_name):
        return {"settings": self}


@register_setting
class SiteSettings(DraftStateMixin, RevisionMixin, PreviewableMixin, BaseGenericSetting):
    """Настройки сайта"""
    name = models.CharField(max_length=100, 
                            verbose_name="Название компании",
                            default="Название компании", 
                            blank=True  )
    icon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Логотип компании",
    )
    address = models.TextField(max_length=100, verbose_name="г.Тюмень",blank=True,)

    content_panels = [
        FieldPanel("name"),
        FieldPanel("icon"),
        FieldPanel("address"),
    ]

    publish_panels = [
        PublishingPanel(),
    ]



    class Meta:
        verbose_name = "Настройки сайта"

    def get_preview_template(self, request, mode_name):
        return "base.html"

    def get_preview_context(self, request, mode_name):
        return {"settings": self}