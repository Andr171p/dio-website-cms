from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock


class FeedbackFormBlock(blocks.StructBlock):
    """Блок формы обратной связи"""
    form_title = blocks.CharBlock(
        required=False, default="Свяжитесь с нами", label="Заголовок формы"
    )
    form_description = blocks.TextBlock(
        required=False, label="Описание формы"
    )
    success_message = blocks.CharBlock(
        required=False,
        default="Спасибо! Ваше сообщение отправлено.",
        label="Сообщение об успешной отправке"
    )

    class Meta:
        icon = "form"
        label = "Форма обратной связи"


class ContactsBlock(blocks.StructBlock):
    """Блок контактов компании"""
    section_title = blocks.CharBlock(
        required=False,
        default="Контакты",
        label="Заголовок секции"
    )
    show_map = blocks.BooleanBlock(
        required=False,
        default=True,
        label="Показывать карту"
    )
    map_embed = EmbedBlock(
        required=False,
        label="Код embed карты",
        help_text="Вставьте embed код карты из Yandex Maps, Google Maps, ..."
    )
    contact_items = blocks.ListBlock(
        blocks.PageChooserBlock(
            page_type=None, label="Контакты"
        ),
        required=False,
        label="Выбранные контакты"
    )

    class Meta:
        icon = "group"
        label = "Блок контактов"
