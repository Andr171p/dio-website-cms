from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.api import APIField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.api.fields import ImageRenditionField as ImageAPIField
from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.api.fields import ImageRenditionField


# Create your models here.

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