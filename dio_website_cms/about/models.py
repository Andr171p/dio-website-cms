from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField, RichTextField
from wagtail.models import Page
from wagtail.api import APIField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.api.fields import ImageRenditionField as ImageAPIField
from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from home.models import MainAchievementBlock,AdditionalAchievementBlock, GlobalPresenceBlock

# Create your models here.
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

    global_presence = StreamField(
        [
            ("presence", GlobalPresenceBlock()),  # Это имя должно совпадать с block.block_type
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Глобальное присутствие",
        max_num=1,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("global_presence"),
            ],
            heading="Секция 'Глобальное присутствие'",
        ),
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
        APIField("global_presence"),
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
        from home.models import HomePage
        home_page = HomePage.objects.live().first()
        if home_page:
            context['home_global_presence'] = home_page.global_presence
        context["hero_service_list_items"] = self.hero_service_list.split("\n") if self.hero_service_list else []
        context["career_items_list"] = self.career_items.split("\n") if self.career_items else []
        return context
  

    class Meta:
        verbose_name = "Страница 'О компании'"
        verbose_name_plural = "Страницы 'О компании'"



