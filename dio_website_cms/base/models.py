from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PublishingPanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail import blocks
from wagtail.fields import StreamField, RichTextField
from wagtail.blocks import (
    PageChooserBlock,
    CharBlock,
    URLBlock,
    TextBlock,
    StructBlock,
    ListBlock,
    ChoiceBlock,
    BooleanBlock,
)
from wagtail.models import DraftStateMixin, RevisionMixin, PreviewableMixin, Page


# ========== HEADER SETTINGS ==========
@register_setting
class HeaderSettings(
    DraftStateMixin, RevisionMixin, PreviewableMixin, BaseGenericSetting
):
    """Настройки хедера сайта"""

    class Meta:
        verbose_name = "Настройки хедера"
        verbose_name_plural = "Настройки хедеров"

    # Основные поля
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Логотип сайта (рекомендуемый размер: 40x40px)",
    )
    site_title = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Название сайта, отображаемое рядом с логотипом",
    )
    consultation_button_text = models.CharField(
        max_length=255, default="Оставить заявку", help_text="Текст кнопки консультации"
    )
    consultation_button_url = models.URLField(
        blank=True, help_text="URL для кнопки консультации"
    )

    # Поле для элементов навигации (StreamField)
    nav_items = StreamField(
        [
            (
                "nav_item",
                StructBlock(
                    [
                        (
                            "name",
                            CharBlock(
                                max_length=255,
                                required=True,
                                label="Название пункта*",
                                help_text="Название пункта меню",
                            ),
                        ),
                        (
                            "page",
                            PageChooserBlock(
                                required=False,
                                label="Страница",
                                help_text="Выберите страницу для ссылки",
                            ),
                        ),
                        (
                            "external_url",
                            URLBlock(
                                required=False,
                                label="Внешняя ссылка",
                                help_text="Укажите внешний URL, если страница не выбрана",
                            ),
                        ),
                        (
                            "menu_type",
                            ChoiceBlock(
                                choices=[
                                    ("none", "Без подменю"),
                                    ("simple", "Простое подменю"),
                                    ("grouped", "Группированное подменю с карточкой"),
                                ],
                                default="none",
                                label="Тип меню*",
                                help_text="Выберите тип подменю: без подменю, простое подменю или группированное подменю с карточкой",
                            ),
                        ),
                        (
                            "simple_dropdown_items",
                            ListBlock(
                                StructBlock(
                                    [
                                        (
                                            "name",
                                            CharBlock(
                                                max_length=255,
                                                required=True,
                                                label="Название подпункта*",
                                                help_text="Название подпункта",
                                            ),
                                        ),
                                        (
                                            "page",
                                            PageChooserBlock(
                                                required=False,
                                                label="Страница",
                                                help_text="Выберите страницу для ссылки",
                                            ),
                                        ),
                                        (
                                            "external_url",
                                            URLBlock(
                                                required=False,
                                                label="Внешняя ссылка",
                                                help_text="Укажите внешний URL, если страница не выбрана",
                                            ),
                                        ),
                                    ]
                                ),
                                required=False,
                                label="Простые элементы подменю",
                                help_text='Используется, если выбран тип "Простое подменю"',
                            ),
                        ),
                        (
                            "dropdown_groups",
                            ListBlock(
                                StructBlock(
                                    [
                                        (
                                            "group_title",
                                            CharBlock(
                                                max_length=255,
                                                required=True,
                                                label="Название группы*",
                                                help_text="Например: Автоматизация бизнеса",
                                            ),
                                        ),
                                        (
                                            "items",
                                            ListBlock(
                                                StructBlock(
                                                    [
                                                        (
                                                            "name",
                                                            CharBlock(
                                                                max_length=255,
                                                                required=True,
                                                                label="Название подпункта*",
                                                                help_text="Название подпункта",
                                                            ),
                                                        ),
                                                        (
                                                            "page",
                                                            PageChooserBlock(
                                                                required=False,
                                                                label="Страница",
                                                                help_text="Выберите страницу для ссылки",
                                                            ),
                                                        ),
                                                        (
                                                            "external_url",
                                                            URLBlock(
                                                                required=False,
                                                                label="Внешняя ссылка",
                                                                help_text="Укажите внешний URL, если страница не выбрана",
                                                            ),
                                                        ),
                                                        (
                                                            "description",
                                                            TextBlock(
                                                                required=False,
                                                                label="Описание",
                                                                help_text="Краткое описание подпункта",
                                                            ),
                                                        ),
                                                        (
                                                            "icon_svg",
                                                            TextBlock(
                                                                required=False,
                                                                label="SVG код иконки",
                                                                help_text="Вставьте SVG код для иконки",
                                                            ),
                                                        ),
                                                    ]
                                                ),
                                                required=False,
                                                label="Элементы подменю",
                                            ),
                                        ),
                                    ]
                                ),
                                required=False,
                                label="Группы выпадающего меню",
                                help_text='Используется, если выбран тип "Группированное подменю"',
                                max_num=3,  # Ограничение до 3 групп
                            ),
                        ),
                        (
                            "card_link",
                            StructBlock(
                                [
                                    (
                                        "enabled",
                                        blocks.BooleanBlock(
                                            default=False,
                                            required=False,
                                            label="Включить карточку",
                                            help_text="Включить карточку ссылки",
                                        ),
                                    ),
                                    (
                                        "title",
                                        CharBlock(
                                            max_length=255,
                                            required=False,
                                            label="Название карточки",
                                            help_text="Название карточки",
                                        ),
                                    ),
                                    (
                                        "description",
                                        TextBlock(
                                            required=False,
                                            label="Описание карточки",
                                            help_text="Описание карточки",
                                        ),
                                    ),
                                    (
                                        "page",
                                        PageChooserBlock(
                                            required=False,
                                            label="Страница",
                                            help_text="Выберите страницу для ссылки",
                                        ),
                                    ),
                                    (
                                        "external_url",
                                        URLBlock(
                                            required=False,
                                            label="Внешняя ссылка",
                                            help_text="Укажите внешний URL, если страница не выбрана",
                                        ),
                                    ),
                                    (
                                        "button_text",
                                        CharBlock(
                                            max_length=255,
                                            default="Подробнее",
                                            required=False,
                                            label="Текст кнопки*",
                                            help_text="Текст кнопки на карточке",
                                        ),
                                    ),
                                ],
                                required=False,
                                label="Карточка ссылки",
                            ),
                        ),
                    ],
                    icon="list-ul",
                    label="Пункт меню",
                ),
            )
        ],
        use_json_field=True,
        blank=True,
        null=True,
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("logo"),
                FieldPanel("site_title"),
                FieldPanel("consultation_button_text"),
                FieldPanel("consultation_button_url"),
                FieldPanel("nav_items"),
            ],
            heading="Основные настройки header",
        ),
        PublishingPanel(),
    ]

    def get_preview_template(self, request, mode_name):
        return "base.html"

    def get_preview_context(self, request, mode_name):
        return {"settings": self}


# ========== FOOTER SETTINGS ==========
# base/models.py или где определена ваша модель


@register_setting
class FooterSettings(
    DraftStateMixin, RevisionMixin, PreviewableMixin, BaseGenericSetting
):
    """Настройки футера сайта"""

    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Логотип сайта",
        help_text="Логотип для footer. Рекомендуемый размер: 40x40px",
    )
    # Основные настройки
    copyright_text = models.CharField(
        max_length=200,
        default="© 2025 Все права защищены",
        verbose_name="Текст копирайта",
    )
    company_address = models.TextField(blank=True, verbose_name="Адрес компании")
    working_hours = models.CharField(
        max_length=100, blank=True, verbose_name="Часы работы"
    )

    # Социальные сети
    social_links = StreamField(
        [
            (
                "social",
                blocks.StructBlock(
                    [
                        (
                            "platform",
                            blocks.CharBlock(max_length=50, label="Платформа"),
                        ),
                        (
                            "href",
                            blocks.CharBlock(
                                max_length=200,
                                label="Ссылка (например, https://facebook.com или #contact)",
                            ),
                        ),
                        (
                            "icon",
                            blocks.CharBlock(
                                max_length=50,
                                label="Иконка (например, facebook, twitter)",
                            ),
                        ),
                    ],
                    label="Социальная сеть",
                ),
            )
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Социальные сети",
    )

    # Секции ссылок
    company_section = StreamField(
        [
            (
                "item",
                blocks.StructBlock(
                    [
                        (
                            "title",
                            blocks.CharBlock(
                                max_length=100, label="Заголовок секции", required=False
                            ),
                        ),
                        (
                            "links",
                            blocks.ListBlock(
                                blocks.StructBlock(
                                    [
                                        (
                                            "text",
                                            blocks.CharBlock(
                                                max_length=100, label="Текст ссылки"
                                            ),
                                        ),
                                        (
                                            "href",
                                            blocks.CharBlock(
                                                max_length=200,
                                                label="Ссылка (например, /about или #contact)",
                                                blank=True,
                                            ),
                                        ),
                                    ]
                                )
                            ),
                        ),
                    ],
                    label="Секция компании",
                ),
            )
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Секции компании",
    )

    solutions_section = StreamField(
        [
            (
                "item",
                blocks.StructBlock(
                    [
                        (
                            "title",
                            blocks.CharBlock(
                                max_length=100, label="Заголовок секции", required=False
                            ),
                        ),
                        (
                            "links",
                            blocks.ListBlock(
                                blocks.StructBlock(
                                    [
                                        (
                                            "text",
                                            blocks.CharBlock(
                                                max_length=100, label="Текст ссылки"
                                            ),
                                        ),
                                        (
                                            "href",
                                            blocks.CharBlock(
                                                max_length=200,
                                                label="Ссылка (например, /solutions или #solutions)",
                                                blank=True,
                                            ),
                                        ),
                                    ]
                                )
                            ),
                        ),
                    ],
                    label="Секция решений",
                ),
            )
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Секции решений",
    )

    services_section = StreamField(
        [
            (
                "item",
                blocks.StructBlock(
                    [
                        (
                            "title",
                            blocks.CharBlock(
                                max_length=100, label="Заголовок секции", required=False
                            ),
                        ),
                        (
                            "links",
                            blocks.ListBlock(
                                blocks.StructBlock(
                                    [
                                        (
                                            "text",
                                            blocks.CharBlock(
                                                max_length=100, label="Текст ссылки"
                                            ),
                                        ),
                                        (
                                            "href",
                                            blocks.CharBlock(
                                                max_length=200,
                                                label="Ссылка (например, /services или #services)",
                                                blank=True,
                                            ),
                                        ),
                                    ]
                                )
                            ),
                        ),
                    ],
                    label="Секция услуг",
                ),
            )
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Секции услуг",
    )

    # Кнопка "Связаться с нами"
    contact_button_text = models.CharField(
        max_length=50, default="Связаться с нами", verbose_name="Текст кнопки"
    )
    contact_button_href = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Ссылка кнопки (например, #contact или /contact)",
    )

    # Панели админки
    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel("copyright_text"),
                FieldPanel("company_address"),
                FieldPanel("working_hours"),
                FieldPanel("social_links"),
                FieldPanel("company_section"),
                FieldPanel("solutions_section"),
                FieldPanel("services_section"),
                FieldPanel("contact_button_text"),
                FieldPanel("contact_button_href"),
            ],
            heading="Настройки футера",
        ),
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
class ContactSettings(
    DraftStateMixin, RevisionMixin, PreviewableMixin, BaseGenericSetting
):
    """Настройки контактов"""

    section_title = models.CharField(
        max_length=100, default="Связаться с нами", verbose_name="Заголовок секции"
    )
    section_description = models.TextField(
        default="Готовы обсудить автоматизацию вашего бизнеса? Свяжитесь с нашими экспертами для получения персональной консультации.",
        verbose_name="Описание секции",
    )
    # Контактная информация
    primary_phone = models.CharField(
        max_length=20, blank=True, verbose_name="Основной телефон"
    )
    secondary_phone = models.CharField(
        max_length=20, blank=True, verbose_name="Дополнительный телефон"
    )
    primary_email = models.EmailField(blank=True, verbose_name="Основной email")
    secondary_email = models.EmailField(blank=True, verbose_name="Дополнительный email")
    address = models.TextField(blank=True, verbose_name="Адрес")
    working_hours = models.TextField(
        default="Пн-Пт: 9:00 - 18:00, Сб-Вс: по договоренности",
        verbose_name="Режим работы",
    )
    map_placeholder_text = models.TextField(
        default="г. Москва, ул. Тверская, д. 15", verbose_name="Текст под картой"
    )
    # Услуги
    services = StreamField(
        [("service", CharBlock(max_length=100, label="Название услуги"))],
        blank=True,
        use_json_field=True,
        verbose_name="Список услуг",
    )
    # Форма
    form_title = models.CharField(
        max_length=100, default="Оставить заявку", verbose_name="Заголовок формы"
    )
    privacy_policy_text = models.TextField(
        default="Нажимая кнопку, вы соглашаетесь с <a href='/privacy-policy/'>политикой обработки персональных данных</a>",
        verbose_name="Текст политики конфиденциальности",
    )

    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel("section_title"),
                FieldPanel("section_description"),
                FieldPanel("primary_phone"),
                FieldPanel("secondary_phone"),
                FieldPanel("primary_email"),
                FieldPanel("secondary_email"),
                FieldPanel("address"),
                FieldPanel("working_hours"),
                FieldPanel("map_placeholder_text"),
                FieldPanel("services"),
                FieldPanel("form_title"),
                FieldPanel("privacy_policy_text"),
            ],
            heading="Настройки контактов",
        ),
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
class SiteSettings(BaseGenericSetting):
    """Настройки сайта"""

    name = models.CharField(
        max_length=100,
        verbose_name="Название компании",
        default="Название компании",
        blank=True,
    )
    icon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Логотип компании",
    )
    address = models.TextField(
        max_length=100,
        verbose_name="г.Тюмень",
        blank=True,
    )

    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("icon"),
                FieldPanel("address"),
            ],
            heading="Основные настройки",
        ),
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


class ContactPage(Page):
    """Страница контактов"""

    # Поля для контактов
    address = models.TextField(blank=True, verbose_name="Адрес")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Электронная почта")
    map_info = models.TextField(
        blank=True, verbose_name="Инструкции для карты (например, Embed-код)"
    )
    contact_form_text = models.TextField(blank=True, verbose_name="Текст для формы")
    legal_name = models.CharField(
        max_length=200, blank=True, verbose_name="Юридическое название"
    )
    inn = models.CharField(max_length=12, blank=True, verbose_name="ИНН")
    ogrn = models.CharField(max_length=13, blank=True, verbose_name="ОГРН")

    # Панели для админки
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("address"),
                FieldPanel("phone"),
                FieldPanel("email"),
            ],
            heading="Контактная информация",
        ),
        FieldPanel("map_info"),
        FieldPanel("contact_form_text"),
        MultiFieldPanel(
            [
                FieldPanel("legal_name"),
                FieldPanel("inn"),
                FieldPanel("ogrn"),
            ],
            heading="Юридические данные",
        ),
    ]

    # Указываем шаблон
    template = "contact/contact_page.html"
