from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PublishingPanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail import blocks
from wagtail.fields import StreamField, RichTextField
from wagtail.blocks import  PageChooserBlock, CharBlock, URLBlock, TextBlock, StructBlock, ListBlock, ChoiceBlock, BooleanBlock
from wagtail.models import DraftStateMixin, RevisionMixin, PreviewableMixin,Page
from django.contrib.auth.models import User
from django import forms 
from wagtail.api import APIField
from wagtail.blocks import CharBlock, RichTextBlock, StructBlock, ListBlock, IntegerBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
# settings/models.py
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.api.fields import ImageRenditionField as ImageAPIField
from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PublishingPanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    StructBlock,
    ListBlock,
    TextBlock,
    BooleanBlock,
    PageChooserBlock,
    URLBlock,
)
from wagtail.models import DraftStateMixin, RevisionMixin, PreviewableMixin
from wagtail.fields import StreamField
from home.models import MainAchievementBlock,AdditionalAchievementBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.api.fields import ImageRenditionField



@register_setting
class HeaderSettings(DraftStateMixin, RevisionMixin, PreviewableMixin, BaseGenericSetting):
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
        max_length=255,
        default="Оставить заявку",
        help_text="Текст кнопки консультации",
    )
    consultation_page = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Выберите страницу для ссылки на консультацию",
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
                            help_text="Выберите тип подменю",
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
                            help_text="Используется для типа 'Простое подменю'",
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
                            help_text="Используется для типа 'Группированное подменю'",
                            max_num=3,  # Ограничение до 3 групп
                        ),
                    ),
                    (
                        "card_link",
                        StructBlock(
                            [
                                (
                                    "enabled",
                                    BooleanBlock(
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
    )],
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
                FieldPanel("consultation_page"),
                FieldPanel("nav_items"),
            ],
            heading="Основные настройки хедера",
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
class FooterSettings(DraftStateMixin, RevisionMixin, PreviewableMixin, BaseGenericSetting):
    """Настройки футера сайта"""
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Логотип сайта",
        help_text="Логотип для footer. Рекомендуемый размер: 40x40px"
    )
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
        ("social", blocks.StructBlock([
            ("platform", blocks.CharBlock(max_length=50, label="Платформа")),
            ("href", blocks.CharBlock(max_length=200, label="Ссылка (например, https://facebook.com или #contact)")),
            ("icon", blocks.CharBlock(max_length=50, label="Иконка (например, facebook, twitter)")),
        ], label="Социальная сеть"))
    ], blank=True, use_json_field=True, verbose_name="Социальные сети")

    # Секции ссылок
    company_section = StreamField([
        ("item", blocks.StructBlock([
            ("title", blocks.CharBlock(max_length=100, label="Заголовок секции", required=False)),
            ("links", blocks.ListBlock(blocks.StructBlock([
                ("text", blocks.CharBlock(max_length=100, label="Текст ссылки")),
                ("href", blocks.CharBlock(max_length=200, label="Ссылка (например, /about или #contact)", blank=True)),
            ])))
        ], label="Секция компании"))
    ], blank=True, use_json_field=True, verbose_name="Секции компании")

    solutions_section = StreamField([
        ("item", blocks.StructBlock([
            ("title", blocks.CharBlock(max_length=100, label="Заголовок секции", required=False)),
            ("links", blocks.ListBlock(blocks.StructBlock([
                ("text", blocks.CharBlock(max_length=100, label="Текст ссылки")),
                ("href", blocks.CharBlock(max_length=200, label="Ссылка (например, /solutions или #solutions)", blank=True)),
            ])))
        ], label="Секция решений"))
    ], blank=True, use_json_field=True, verbose_name="Секции решений")

    services_section = StreamField([
        ("item", blocks.StructBlock([
            ("title", blocks.CharBlock(max_length=100, label="Заголовок секции", required=False)),
            ("links", blocks.ListBlock(blocks.StructBlock([
                ("text", blocks.CharBlock(max_length=100, label="Текст ссылки")),
                ("href", blocks.CharBlock(max_length=200, label="Ссылка (например, /services или #services)", blank=True)),
            ])))
        ], label="Секция услуг"))
    ], blank=True, use_json_field=True, verbose_name="Секции услуг")

    # Кнопка "Связаться с нами"
    contact_button_text = models.CharField(
        max_length=50,
        default="Связаться с нами",
        verbose_name="Текст кнопки"
    )
    contact_button_href = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Ссылка кнопки (например, #contact или /contact)"
    )

    # Панели админки
    content_panels = [
        MultiFieldPanel([
            FieldPanel("copyright_text"),
            FieldPanel("company_address"),
            FieldPanel("working_hours"),
            FieldPanel("social_links"),
            FieldPanel("company_section"),
            FieldPanel("solutions_section"),
            FieldPanel("services_section"),
            FieldPanel("contact_button_text"),
            FieldPanel("contact_button_href"),
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

class ContactSubmission(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    message = models.TextField(verbose_name="Сообщение")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    panels = [
        FieldPanel("name"),
        FieldPanel("email"),
        FieldPanel("phone"),
        FieldPanel("message"),
        FieldPanel("submitted_at"),
    ]

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"Заявка от {self.name} ({self.email})"


@register_setting
class ContactSettings(DraftStateMixin, RevisionMixin, PreviewableMixin, BaseGenericSetting):
    """Настройки контактов"""
    form_recipient_email = models.EmailField(
        blank=True,
        verbose_name="Email для заявок",
        help_text="Email, на который будут отправляться заявки из формы."
    )

    notification_users = models.ManyToManyField(
        User,
        blank=True,
        verbose_name="Пользователи для уведомлений",
        help_text="Выберите пользователей, которые будут получать уведомления в админке."
    )
    section_title = models.CharField(
        max_length=100,
        default="Связаться с нами",
        verbose_name="Заголовок секции"
    )
    section_description = models.TextField(
        default="Готовы обсудить автоматизацию вашего бизнеса? Свяжитесь с нашими экспертами для получения персональной консультации.",
        verbose_name="Описание секции"
    )
    # Контактная информация
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
    working_hours = models.TextField(
        default="Пн-Пт: 9:00 - 18:00, Сб-Вс: по договоренности",
        verbose_name="Режим работы"
    )
    map_placeholder_text = models.TextField(
        default="г. Москва, ул. Тверская, д. 15",
        verbose_name="Текст под картой"
    )
    # Услуги
    services = StreamField([
        ("service", CharBlock(max_length=100, label="Название услуги"))
    ], blank=True, use_json_field=True, verbose_name="Список услуг")
    # Форма
    form_title = models.CharField(
        max_length=100,
        default="Оставить заявку",
        verbose_name="Заголовок формы"
    )
    privacy_policy_text = models.TextField(
        default="Нажимая кнопку, вы соглашаетесь с <a href='/privacy-policy/'>политикой обработки персональных данных</a>",
        verbose_name="Текст политики конфиденциальности"
    )

    content_panels = [
        MultiFieldPanel([
            FieldPanel("form_recipient_email"),
            FieldPanel("notification_users", widget=forms.CheckboxSelectMultiple),
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
        ], heading="Настройки контактов"),
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
        blank=True
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
        MultiFieldPanel([
            FieldPanel("name"),
            FieldPanel("icon"),
            FieldPanel("address"),
        ], heading="Основные настройки"),
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



class AboutPage(Page):
    """Страница 'О компании' с полным набором редактируемых полей"""

    achievements = StreamField(
        [
            ("main_achievement", MainAchievementBlock()),
            ("additional_achievement", AdditionalAchievementBlock()),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Достижения",
    )

    # Hero/About секция
    hero_title = models.CharField(
        max_length=255,
        blank=True,
        default="О компании",
        help_text="Заголовок секции 'О компании'",
    )
    hero_description_1 = RichTextField(
        blank=True,
        help_text="Первое описание компании в секции Hero",
        default="Группа ALMA — надёжный партнёр нефтегазовых и нефтесервисных компаний в РФ и за рубежом",
    )
    hero_description_2 = RichTextField(
        blank=True,
        help_text="Второе описание компании в секции Hero",
        default="Разрабатываем собственные программные решения для отраслей",
    )
    hero_description_3 = RichTextField(
        blank=True,
        help_text="Третье описание компании в секции Hero",
        default="Внедряем ИИ и ML в процессы управления производством, предиктивного анализа, автоматизации",
    )
    hero_service_list = models.TextField(
        blank=True,
        help_text="Список сервисов и услуг (каждый пункт с новой строки)",
        default="IT-компании и ИТ-подразделения\nПромышленные и технологические предприятия\nОрганизации, стремящиеся повысить эффективность управления",
    )
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение для секции 'О компании'",
    )
    hero_button_text = models.CharField(
        max_length=50,
        blank=True,
        default="Связаться с нами",
        help_text="Текст кнопки в секции Hero",
    )
    hero_button_link = models.CharField(
        max_length=255,
        blank=True,
        default="#contact",
        help_text="Ссылка для кнопки в секции Hero",
    )

    # Industries/Отрасли секция
    industries_title = models.CharField(
        max_length=255,
        blank=True,
        default="Отрасли применения",
        help_text="Заголовок секции 'Отрасли'",
    )
    industry_01 = models.CharField(
        max_length=100,
        blank=True,
        default="Нефтегазовая промышленность",
        help_text="Отрасль 01",
    )
    industry_02 = models.CharField(
        max_length=100,
        blank=True,
        default="Химическая промышленность",
        help_text="Отрасль 02",
    )
    industry_03 = models.CharField(
        max_length=100,
        blank=True,
        default="Металлургическая промышленность",
        help_text="Отрасль 03",
    )
    industry_04 = models.CharField(
        max_length=100,
        blank=True,
        default="Гражданское строительство",
        help_text="Отрасль 04",
    )
    industry_05 = models.CharField(
        max_length=100,
        blank=True,
        default="Пищевая промышленность",
        help_text="Отрасль 05",
    )
    industry_06 = models.CharField(
        max_length=100,
        blank=True,
        default="Электроэнергетика",
        help_text="Отрасль 06",
    )

    # Trust/Metrics/Facts секция
    trust_title = models.CharField(
        max_length=255,
        blank=True,
        default="Нам доверяют",
        help_text="Заголовок секции 'Метрики'",
    )
    metric_year_label = models.CharField(
        max_length=50,
        blank=True,
        default="Год основания компании",
        help_text="Заголовок метрики года",
    )
    metric_year_value = models.CharField(
        max_length=50,
        blank=True,
        default="2017",
        help_text="Значение метрики года",
    )
    metric_projects_label = models.CharField(
        max_length=50,
        blank=True,
        default="Реализованных проектов",
        help_text="Заголовок метрики проектов",
    )
    metric_projects_value = models.CharField(
        max_length=50,
        blank=True,
        default="35+",
        help_text="Значение метрики проектов",
    )
    metric_presence_label = models.CharField(
        max_length=50,
        blank=True,
        default="Глобальное присутствие",
        help_text="Заголовок метрики присутствия",
    )
    metric_presence_value = models.CharField(
        max_length=50,
        blank=True,
        default="Россия / международно",
        help_text="Значение метрики присутствия",
    )

    # Approach/Value секция
    approach_title = models.CharField(
        max_length=255,
        blank=True,
        default="Комплексный подход",
        help_text="Заголовок секции 'Подход и ценность'",
    )
    approach_description_1 = RichTextField(
        blank=True,
        help_text="Первый пункт описания подхода",
        default="Полная интеграция ИТ-систем в бизнес-процессы компании для повышения прозрачности и управляемости",
    )
    approach_description_2 = RichTextField(
        blank=True,
        help_text="Второй пункт описания подхода",
        default="Переход на управление в режиме реального времени и постоянное внедрение улучшений для устойчивого роста",
    )

    # Career/Карьера секция
    career_title = models.CharField(
        max_length=255,
        blank=True,
        default="Карьера в ALMA",
        help_text="Заголовок секции 'Карьера'",
    )
    career_description = RichTextField(
        blank=True,
        help_text="Описание секции 'Карьера'",
        default="ALMA — команда профессионалов, работающих с крупными нефтегазовыми компаниями. У нас гибкая система бонусов, удалёнка, рост, открытые отношения внутри команды.",
    )
    career_button_text = models.CharField(
        max_length=50,
        blank=True,
        default="Подробнее",
        help_text="Текст кнопки в секции 'Карьера'",
    )
    career_button_link = models.CharField(
        max_length=255,
        blank=True,
        default="#",
        help_text="Ссылка для кнопки в секции 'Карьера'",
    )
    career_items = models.TextField(
        blank=True,
        help_text="Список направлений карьеры (каждый пункт с новой строки)",
        default="Проектное управление\nФинансовый анализ\nУправление производством\nИнженерные решения\nРазработка интерфейсов\nСерверная разработка\nUI/UX-дизайн\nГрафический дизайн\nАнализ данных\nЦифровой маркетинг",
    )

    # Contact секция
    contact_title = models.CharField(
        max_length=255,
        blank=True,
        default="Связаться с нами",
        help_text="Заголовок секции 'Контакты'",
    )
    contact_description = models.TextField(
        blank=True,
        help_text="Описание секции 'Контакты'",
        default="Нажимая кнопку, я принимаю соглашение о конфиденциальности и соглашаюсь с обработкой персональных данных",
    )
    contact_privacy_note = models.TextField(
        blank=True,
        help_text="Примечание о конфиденциальности",
        default="This site is protected by reCAPTCHA and the Google Privacy Policy and Terms of Service apply.",
    )
    contact_button_text = models.CharField(
        max_length=50,
        blank=True,
        default="Отправить",
        help_text="Текст кнопки в секции 'Контакты'",
    )
    contact_button_link = models.CharField(
        max_length=255,
        blank=True,
        default="#",
        help_text="Ссылка для кнопки в секции 'Контакты'",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_title"),
                FieldPanel("hero_description_1"),
                FieldPanel("hero_description_2"),
                FieldPanel("hero_description_3"),
                FieldPanel("hero_service_list"),
                FieldPanel("hero_image"),
                FieldPanel("hero_button_text"),
                FieldPanel("hero_button_link"),
            ],
            heading="Секция 'О компании' (Hero)",
        ),
        MultiFieldPanel(
            [
                FieldPanel("industries_title"),
                FieldPanel("industry_01"),
                FieldPanel("industry_02"),
                FieldPanel("industry_03"),
                FieldPanel("industry_04"),
                FieldPanel("industry_05"),
                FieldPanel("industry_06"),
            ],
            heading="Секция 'Отрасли'",
        ),
        MultiFieldPanel(
            [
                FieldPanel("trust_title"),
                FieldPanel("metric_year_label"),
                FieldPanel("metric_year_value"),
                FieldPanel("metric_projects_label"),
                FieldPanel("metric_projects_value"),
                FieldPanel("metric_presence_label"),
                FieldPanel("metric_presence_value"),
            ],
            heading="Секция 'Метрики'",
        ),
        MultiFieldPanel(
            [
                FieldPanel("approach_title"),
                FieldPanel("approach_description_1"),
                FieldPanel("approach_description_2"),
            ],
            heading="Секция 'Подход и ценность'",
        ),
        MultiFieldPanel(
            [
                FieldPanel("career_title"),
                FieldPanel("career_description"),
                FieldPanel("career_button_text"),
                FieldPanel("career_button_link"),
                FieldPanel("career_items"),
            ],
            heading="Секция 'Карьера'",
        ),
        MultiFieldPanel(
            [
                FieldPanel("contact_title"),
                FieldPanel("contact_description"),
                FieldPanel("contact_privacy_note"),
                FieldPanel("contact_button_text"),
                FieldPanel("contact_button_link"),
            ],
            heading="Секция 'Контакты'",
        ),
        MultiFieldPanel(
            [
                FieldPanel("achievements"),
            ],
            heading="Достижения",
        ),
    ]

    api_fields = [
        APIField("hero_title"),
        APIField("hero_description_1"),
        APIField("hero_description_2"),
        APIField("hero_description_3"),
        APIField("hero_service_list"),
        APIField("hero_image"),
        APIField("hero_button_text"),
        APIField("hero_button_link"),
        APIField("industries_title"),
        APIField("industry_01"),
        APIField("industry_02"),
        APIField("industry_03"),
        APIField("industry_04"),
        APIField("industry_05"),
        APIField("industry_06"),
        APIField("trust_title"),
        APIField("metric_year_label"),
        APIField("metric_year_value"),
        APIField("metric_projects_label"),
        APIField("metric_projects_value"),
        APIField("metric_presence_label"),
        APIField("metric_presence_value"),
        APIField("approach_title"),
        APIField("approach_description_1"),
        APIField("approach_description_2"),
        APIField("career_title"),
        APIField("career_description"),
        APIField("career_button_text"),
        APIField("career_button_link"),
        APIField("career_items"),
        APIField("contact_title"),
        APIField("contact_description"),
        APIField("contact_privacy_note"),
        APIField("contact_button_text"),
        APIField("contact_button_link"),
        APIField("achievements"),
    ]

    def get_context(self, request, *args, **kwargs):
        from services.models import ServiceBlock

        context = super().get_context(request, *args, **kwargs)
        context["main_achievements"] = [
            block
            for block in self.achievements
            if block.block_type == "main_achievement"
        ]
        context["additional_achievements"] = [
            block
            for block in self.achievements
            if block.block_type == "additional_achievement"
        ]
        context["hero_service_list_items"] = self.hero_service_list.split("\n") if self.hero_service_list else []
        context["career_items_list"] = self.career_items.split("\n") if self.career_items else []
        return context

    class Meta:
        verbose_name = "Страница 'О компании'"
        verbose_name_plural = "Страницы 'О компании'"




class CareerPage(Page):
    """Страница 'Карьера' на основе структуры сайта ALMA."""

    # Секция Hero
    hero_title = models.CharField(
        max_length=255,
        blank=True,
        default="Карьера",
        help_text="Заголовок секции Hero",
    )
    hero_description = RichTextField(
        blank=True,
        features=['bold', 'italic', 'link', 'ol', 'ul', 'hr', 'blockquote'],
        help_text="Основное описание в секции Hero",
        default="ALMA — команда профессионалов, работающая с крупнейшими нефтегазовыми компаниями в России и за её пределами",
    )
    hero_about_link_text = models.CharField(
        max_length=50,
        blank=True,
        default="Подробнее",
        help_text="Текст ссылки на страницу 'О компании'",
    )
    hero_about_link = models.CharField(
        max_length=255,
        blank=True,
        default="/about/",
        help_text="Ссылка на страницу 'О компании'",
    )
    hero_service_list = models.TextField(
        blank=True,
        help_text="Список сервисов и услуг (каждый пункт с новой строки)",
        default="IT-компании и ИТ-подразделения\nПромышленные и технологические предприятия\nОрганизаций, стремящихся повысить эффективность управления",
    )
    hero_additional_descriptions = models.TextField(
        blank=True,
        help_text="Дополнительные описания (каждый абзац с новой строки)",
        default="Разрабатываем собственные программные решения для отраслей\nВнедряем ИИ и ML в процессы управления производством, предиктивного анализа, автоматизации",
    )

    # Метрики в Hero
    metric_year_label = models.CharField(
        max_length=50,
        blank=True,
        default="Год основания компании",
        help_text="Заголовок метрики года",
    )
    metric_year_value = models.CharField(
        max_length=50,
        blank=True,
        default="2017",
        help_text="Значение метрики года",
    )
    metric_projects_label = models.CharField(
        max_length=50,
        blank=True,
        default="Реализованных проектов",
        help_text="Заголовок метрики проектов",
    )
    metric_projects_value = models.CharField(
        max_length=50,
        blank=True,
        default="35+",
        help_text="Значение метрики проектов",
    )

    # Секция "Наши ценности"
    values_title = models.CharField(
        max_length=255,
        blank=True,
        default="Наши ценности",
        help_text="Заголовок секции 'Наши ценности'",
    )
    values_list = models.TextField(
        blank=True,
        help_text="Список ценностей (каждый пункт: 'Заголовок | Описание' с новой строки)",
        default="Вовлечённость и работа на результат | Мы всегда ориентированы на достижение целей и вовлечены в процесс\nИнновации и развитие | Постоянно внедряем новые технологии для роста\nКомандная работа | Поддерживаем друг друга и делимся знаниями",
    )

    # Секция "Карьера в ALMA"
    career_title = models.CharField(
        max_length=255,
        blank=True,
        default="Карьера в ALMA",
        help_text="Заголовок секции 'Карьера в ALMA'",
    )
    advantages_list = models.TextField(
        blank=True,
        help_text="Список преимуществ (каждый пункт с новой строки)",
        default="Гибкий график работы\nВозможность удалёнки\nКонкурентные зарплаты\nПрофессиональный рост\nКорпоративное обучение",
    )

    # Секция направлений/вакансий
    directions_title = models.CharField(
        max_length=255,
        blank=True,
        default="Направления",
        help_text="Заголовок секции 'Направления/Вакансии'",
    )
    directions_list = models.TextField(
        blank=True,
        help_text="Список направлений (каждый пункт: 'Название | Описание' с новой строки)",
        default="Проектное управление | Координация и контроль проектов\nФинансовый анализ | Анализ и планирование финансов\nРазработка ПО | Создание и поддержка программных решений",
    )

    # Секция формы отклика
    form_title = models.CharField(
        max_length=255,
        blank=True,
        default="Хотите в команду?",
        help_text="Заголовок секции формы",
    )
    form_description = RichTextField(
        blank=True,
        features=['bold', 'italic', 'link', 'ol', 'ul', 'hr', 'blockquote'],
        help_text="Описание формы отклика",
        default="Расскажите о своем опыте и кем вы видите себя в ALMA. Оставьте контакты и прикрепите резюме - мы обязательно свяжемся с вами в случае подходящей вакансии.",
    )
    form_privacy_text = models.CharField(
        max_length=255,
        blank=True,
        default="Нажимая кнопку, я принимаю соглашение о конфиденциальности и соглашаюсь с обработкой персональных данных",
        help_text="Текст согласия с политикой конфиденциальности",
    )
    form_privacy_link = models.CharField(
        max_length=255,
        blank=True,
        default="/privacy-policy/",
        help_text="Ссылка на политику конфиденциальности",
    )
    form_recaptcha_note = models.TextField(
        blank=True,
        help_text="Примечание о reCAPTCHA",
        default="This site is protected by reCAPTCHA and the Google Privacy Policy and Terms of Service apply.",
    )

    # Секция "Наш офис"
    office_title = models.CharField(
        max_length=255,
        blank=True,
        default="Наш офис",
        help_text="Заголовок секции 'Наш офис'",
    )
    office_address = models.CharField(
        max_length=255,
        blank=True,
        default="Москва, ул. Примерная, д. 1",
        help_text="Адрес офиса",
    )
    office_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Изображение офиса (опционально)",
    )

    # Панели админки
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_title"),
                FieldPanel("hero_description"),
                FieldPanel("hero_about_link_text"),
                FieldPanel("hero_about_link"),
                FieldPanel("hero_service_list"),
                FieldPanel("hero_additional_descriptions"),
                FieldPanel("metric_year_label"),
                FieldPanel("metric_year_value"),
                FieldPanel("metric_projects_label"),
                FieldPanel("metric_projects_value"),
            ],
            heading="Секция Hero",
        ),
        MultiFieldPanel(
            [
                FieldPanel("values_title"),
                FieldPanel("values_list"),
            ],
            heading="Секция 'Наши ценности'",
        ),
        MultiFieldPanel(
            [
                FieldPanel("career_title"),
                FieldPanel("advantages_list"),
            ],
            heading="Секция 'Карьера в ALMA'",
        ),
        MultiFieldPanel(
            [
                FieldPanel("directions_title"),
                FieldPanel("directions_list"),
            ],
            heading="Секция 'Направления/Вакансии'",
        ),
        MultiFieldPanel(
            [
                FieldPanel("form_title"),
                FieldPanel("form_description"),
                FieldPanel("form_privacy_text"),
                FieldPanel("form_privacy_link"),
                FieldPanel("form_recaptcha_note"),
            ],
            heading="Секция 'Хотите в команду?' (Форма)",
        ),
        MultiFieldPanel(
            [
                FieldPanel("office_title"),
                FieldPanel("office_address"),
                FieldPanel("office_image"),
            ],
            heading="Секция 'Наш офис'",
        ),
    ]

    # API-поля
    api_fields = [
        APIField("hero_title"),
        APIField("hero_description"),
        APIField("hero_about_link_text"),
        APIField("hero_about_link"),
        APIField("hero_service_list"),
        APIField("hero_additional_descriptions"),
        APIField("metric_year_label"),
        APIField("metric_year_value"),
        APIField("metric_projects_label"),
        APIField("metric_projects_value"),
        APIField("values_title"),
        APIField("values_list"),
        APIField("career_title"),
        APIField("advantages_list"),
        APIField("directions_title"),
        APIField("directions_list"),
        APIField("form_title"),
        APIField("form_description"),
        APIField("form_privacy_text"),
        APIField("form_privacy_link"),
        APIField("form_recaptcha_note"),
        APIField("office_title"),
        APIField("office_address"),
        ImageRenditionField("office_image"),
    ]

    def get_context(self, request, *args, **kwargs):
        """Расширяет контекст для шаблона."""
        context = super().get_context(request, *args, **kwargs)
        
        # Hero service list
        context["hero_service_list_items"] = []
        if self.hero_service_list:
            for item in self.hero_service_list.split("\n"):
                stripped = item.strip()
                if stripped:
                    context["hero_service_list_items"].append(stripped)
        
        # Hero additional descriptions
        context["hero_additional_descriptions_items"] = []
        if self.hero_additional_descriptions:
            for item in self.hero_additional_descriptions.split("\n"):
                stripped = item.strip()
                if stripped:
                    context["hero_additional_descriptions_items"].append(stripped)
        
        # Values items (чисто: без дублей и хардкода)
        context["values_items"] = []
        if self.values_list:
            for line in self.values_list.split("\n"):
                line = line.strip()
                if line:  # Только непустые строки
                    parts = line.split("|", 1)
                    title = parts[0].strip() if len(parts) > 0 else line
                    description = parts[1].strip() if len(parts) > 1 else ""
                    context["values_items"].append({"title": title, "description": description})
        
        # Advantages items
        context["advantages_items"] = []
        if self.advantages_list:
            for item in self.advantages_list.split("\n"):
                stripped = item.strip()
                if stripped and len(stripped) > 1:  # Добавил len > 1, чтобы убрать 'вв'-подобные тесты
                    context["advantages_items"].append(stripped)
        
        # Directions items
        context["directions_items"] = []
        if self.directions_list:
            for line in self.directions_list.split("\n"):
                line = line.strip()
                if line:
                    parts = line.split("|", 1)
                    title = parts[0].strip() if len(parts) > 0 else line
                    description = parts[1].strip() if len(parts) > 1 else ""
                    context["directions_items"].append({"title": title, "description": description})
        
        return context

    class Meta:
        verbose_name = "Страница 'Карьера'"
        verbose_name_plural = "Страницы 'Карьера'"