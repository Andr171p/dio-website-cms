from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.blocks import StructBlock, CharBlock, RichTextBlock, ListBlock, TextBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.api import APIField
from wagtail.images.api.fields import ImageRenditionField as ImageAPIField

class HeroBlock(StructBlock):
    title = CharBlock(required=True, max_length=255, help_text="Заголовок секции Hero", default="Карьера")
    description = RichTextBlock(
        required=False,
        features=['bold', 'italic', 'link', 'ol', 'ul', 'hr', 'blockquote'],
        help_text="Основное описание в секции Hero",
        default="ALMA — команда профессионалов, работающая с крупнейшими нефтегазовыми компаниями в России и за её пределами"
    )
    about_link_text = CharBlock(required=False, max_length=50, help_text="Текст ссылки на страницу 'О компании'", default="Подробнее")
    about_link = CharBlock(required=False, max_length=255, help_text="Ссылка на страницу 'О компании'", default="/about/")
    service_list = TextBlock(
        required=False,
        help_text="Список сервисов и услуг (каждый пункт с новой строки)",
        default="IT-компании и ИТ-подразделения\nПромышленные и технологические предприятия\nОрганизаций, стремящихся повысить эффективность управления"
    )
    additional_descriptions = TextBlock(
        required=False,
        help_text="Дополнительные описания (каждый абзац с новой строки)",
        default="Разрабатываем собственные программные решения для отраслей\nВнедряем ИИ и ML в процессы управления производством, предиктивного анализа, автоматизации"
    )
    metrics = ListBlock(
        StructBlock([
            ("label", CharBlock(required=True, max_length=50, help_text="Заголовок метрики")),
            ("value", CharBlock(required=True, max_length=50, help_text="Значение метрики"))
        ]),
        help_text="Список метрик (например, год основания, проекты)"
    )
    image = ImageChooserBlock(required=False, help_text="Изображение для секции Hero")

class ValuesBlock(StructBlock):
    title = CharBlock(required=True, max_length=255, help_text="Заголовок секции 'Наши ценности'", default="Наши ценности")
    values = ListBlock(
        StructBlock([
            ("title", CharBlock(required=True, max_length=255, help_text="Заголовок ценности")),
            ("description", TextBlock(required=False, help_text="Описание ценности"))
        ]),
        help_text="Список ценностей"
    )
    image = ImageChooserBlock(required=False, help_text="Изображение для секции 'Наши ценности'")

class TrustMetricsSection(StructBlock):
    title = CharBlock(required=True, max_length=255, help_text="Заголовок секции 'Преимущества'", default="Карьера в ALMA")
    description = TextBlock(required=False, help_text="Описание секции")
    image = ImageChooserBlock(required=False, help_text="Изображение для секции метрик")
    metrics = ListBlock(
        StructBlock([
            ("value", CharBlock(required=True, max_length=50, help_text="Значение метрики")),
            ("label", CharBlock(required=True, max_length=50, help_text="Подпись метрики")),
            ("icon", TextBlock(required=False, help_text="SVG-код иконки (опционально)"))
        ]),
        help_text="Список метрик"
    )

class DirectionsBlock(StructBlock):
    title = CharBlock(required=True, max_length=255, help_text="Заголовок секции 'Направления/Вакансии'", default="Направления")
    directions = ListBlock(
        StructBlock([
            ("title", CharBlock(required=True, max_length=255, help_text="Название направления")),
            ("description", TextBlock(required=False, help_text="Описание направления"))
        ]),
        help_text="Список направлений"
    )
    image = ImageChooserBlock(required=False, help_text="Изображение для секции 'Направления'")

class FormBlock(StructBlock):
    title = CharBlock(required=True, max_length=255, help_text="Заголовок секции формы", default="Хотите в команду?")
    description = RichTextBlock(
        required=False,
        features=['bold', 'italic', 'link', 'ol', 'ul', 'hr', 'blockquote'],
        help_text="Описание формы отклика",
        default="Расскажите о своем опыте и кем вы видите себя в ALMA. Оставьте контакты и прикрепите резюме - мы обязательно свяжемся с вами в случае подходящей вакансии."
    )
    privacy_text = CharBlock(
        required=False,
        max_length=255,
        help_text="Текст согласия с политикой конфиденциальности",
        default="Нажимая кнопку, я принимаю соглашение о конфиденциальности и соглашаюсь с обработкой персональных данных"
    )
    privacy_link = CharBlock(
        required=False,
        max_length=255,
        help_text="Ссылка на политику конфиденциальности",
        default="/privacy-policy/"
    )
    recaptcha_note = TextBlock(
        required=False,
        help_text="Примечание о reCAPTCHA",
        default="This site is protected by reCAPTCHA and the Google Privacy Policy and Terms of Service apply."
    )
    image = ImageChooserBlock(required=False, help_text="Изображение для секции формы")

class OfficeBlock(StructBlock):
    title = CharBlock(required=True, max_length=255, help_text="Заголовок секции 'Наш офис'", default="Наш офис")
    address = CharBlock(required=False, max_length=255, help_text="Адрес офиса", default="Москва, ул. Примерная, д. 1")
    image = ImageChooserBlock(required=False, help_text="Изображение офиса")

class CareerPage(Page):
    """Страница 'Карьера' с гибкой структурой блоков."""

    content = StreamField(
        [
            ("hero", HeroBlock()),
            ("values", ValuesBlock()),
            ("trust_metrics", TrustMetricsSection()),
            ("directions", DirectionsBlock()),
            ("form", FormBlock()),
            ("office", OfficeBlock()),
        ],
        use_json_field=True,
        blank=True,
        verbose_name="Контент страницы",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("content"),
            ],
            heading="Контент страницы",
        ),
    ]

    api_fields = [
        APIField("content"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["content"] = [
            {
                "type": block.block_type,
                "value": block.value,
                "id": block.id,
                "service_list_items": block.value.get("service_list", "").split("\n") if block.block_type == "hero" and block.value.get("service_list") else [],
                "additional_descriptions_items": block.value.get("additional_descriptions", "").split("\n") if block.block_type == "hero" and block.value.get("additional_descriptions") else [],
            }
            for block in self.content
        ]
        return context

    class Meta:
        verbose_name = "Страница 'Карьера'"
        verbose_name_plural = "Страницы 'Карьера'"