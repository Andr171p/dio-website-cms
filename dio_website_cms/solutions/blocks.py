from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

MAX_TITLE_LENGTH = 120


class SolutionIntroBlock(blocks.StructBlock):
    """Блок с описанием решения/продукта"""
    image = ImageChooserBlock(
        label="Изображение", help_text="Рекомендуемый размер: 600x400px", required=True
    )
    title = blocks.CharBlock(
        max_length=MAX_TITLE_LENGTH, label="Заголовок", help_text="Краткий заголовок карточки"
    )
    description = blocks.TextBlock(
        label="Описание", help_text="Описание продукта", required=True
    )
