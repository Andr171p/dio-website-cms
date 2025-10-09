from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField, RichTextField
from wagtail.models import Page
from wagtail.blocks import StructBlock, CharBlock, RichTextBlock, ListBlock, TextBlock, PageChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.api import APIField
from wagtail.images.api.fields import ImageRenditionField as ImageAPIField
from home.models import MainAchievementBlock, AdditionalAchievementBlock

class HeroBlock(StructBlock):
    title = CharBlock(required=True, help_text="Заголовок секции 'О компании'")
    description_1 = RichTextBlock(required=False, help_text="Первое описание компании")
    description_2 = RichTextBlock(required=False, help_text="Второе описание компании")
    description_3 = RichTextBlock(required=False, help_text="Третье описание компании")
    service_list = TextBlock(required=False, help_text="Список сервисов и услуг (каждый пункт с новой строки)")
    image = ImageChooserBlock(required=False, help_text="Изображение для секции")
    button_text = CharBlock(required=False, max_length=50, help_text="Текст кнопки")
    button_link = PageChooserBlock(required=False, help_text="Ссылка на страницу для кнопки")

class IndustryBlock(StructBlock):
    title = CharBlock(required=True, help_text="Название отрасли")
    description = RichTextBlock(required=False, help_text="Описание отрасли")

class IndustriesSection(StructBlock):
    title = CharBlock(required=True, help_text="Заголовок секции 'Отрасли'")
    industries = ListBlock(IndustryBlock(), help_text="Список отраслей")

class MetricBlock(StructBlock):
    value = CharBlock(required=True, max_length=50, help_text="Значение метрики")
    label = CharBlock(required=True, max_length=50, help_text="Подпись метрики")
    icon = TextBlock(required=False, help_text="SVG-код иконки (опционально)")

class TrustMetricsSection(StructBlock):
    title = CharBlock(required=True, help_text="Заголовок секции 'Метрики'")
    description = TextBlock(required=False, help_text="Описание секции")
    metrics = ListBlock(MetricBlock(), help_text="Список метрик")

class ApproachBlock(StructBlock):
    title = CharBlock(required=True, help_text="Заголовок секции 'Подход'")
    descriptions = ListBlock(RichTextBlock(), help_text="Список описаний подхода")

class CareerBlock(StructBlock):
    title = CharBlock(required=True, help_text="Заголовок секции 'Карьера'")
    description = RichTextBlock(required=False, help_text="Описание секции")
    button_text = CharBlock(required=False, max_length=50, help_text="Текст кнопки")
    button_link = PageChooserBlock(required=False, help_text="Ссылка на страницу для кнопки")
    items = TextBlock(required=False, help_text="Список направлений карьеры (каждый пункт с новой строки)")

class ContactBlock(StructBlock):
    title = CharBlock(required=True, help_text="Заголовок секции 'Контакты'")
    description = TextBlock(required=False, help_text="Описание секции")
    privacy_note = TextBlock(required=False, help_text="Примечание о конфиденциальности")
    button_text = CharBlock(required=False, max_length=50, help_text="Текст кнопки")
    button_link = PageChooserBlock(required=False, help_text="Ссылка на страницу для кнопки")

class AboutPage(Page):
    """Страница 'О компании' с полной гибкостью секций"""

    content = StreamField(
        [
            ("hero", HeroBlock()),
            ("industries", IndustriesSection()),
            ("trust_metrics", TrustMetricsSection()),
            ("approach", ApproachBlock()),
            ("career", CareerBlock()),
            ("contact", ContactBlock()),
            ("main_achievement", MainAchievementBlock()),
            ("additional_achievement", AdditionalAchievementBlock()),
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
                "items_list": block.value.get("items", "").split("\n") if block.block_type == "career" and block.value.get("items") else [],
            }
            for block in self.content
        ]
        return context

    class Meta:
        verbose_name = "Страница 'О компании'"
        verbose_name_plural = "Страницы 'О компании'"