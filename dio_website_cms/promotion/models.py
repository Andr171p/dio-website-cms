from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.search import index
from django.utils import timezone

from wagtail import blocks
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class SinglePromotionPage(Page):
    # template = "single_promotion_page.html"

    date = models.DateField("Дата начала", default=timezone.now)

    end_date = models.DateField("Действует до")

    intro = models.TextField(
        "Описание акции", blank=True, help_text="1-3 предложения для описания акции"
    )

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Изображение",
    )

    button_link = models.URLField("Ссылка кнопки", blank=True)

    content = StreamField(
        [('text', 
          blocks.RichTextBlock(
              features=[ "h2", "h3", "h4",
                        "bold", "italic", "link",
                        "ol", "ul", "blockquote"],
              label="Текстовый блок",)
        )], blank=True, use_json_field=True, verbose_name="Подробности акции")

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("date"),
                FieldPanel("end_date"),
                FieldPanel("intro"),
                FieldPanel("image"),
                FieldPanel("button_link"),
            ],
            heading="Основная информация",
        ),
        MultiFieldPanel(
            [
                FieldPanel('content'),
            ], 
            heading="Подробности акции"
        ),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("title"),
        index.SearchField("intro"),
        index.SearchField("content"),
    ]

    parent_page_types = ["promotion.PromotionIndexPage"]   
    subpage_types = []

    def get_context(self, request):
        context = super().get_context(request)
        context["other_promotions"] = (
            SinglePromotionPage.objects.live().exclude(id=self.id).order_by("-date")[:3]
        )
        return context

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"

class PromotionIndexPage(Page):
    intro = RichTextField("Введение", features=[ "italic", "link"], blank=True)
    items_per_page = models.PositiveIntegerField("Акций на странице", default=9)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("items_per_page"),
    ]

    subpage_types = ['promotion.SinglePromotionPage']
    parent_page_types = ['home.HomePage']

    def get_context(self, request):
        context = super().get_context(request)
        
        today = timezone.now().date()

        promotions = (
            SinglePromotionPage.objects.child_of(self)
            .live()
            .filter(end_date__gte=today)
            .order_by("-date")
        )

        paginator = Paginator(promotions, self.items_per_page)
        page_number  = request.GET.get("page")
        try:
            promotions = paginator.page(page_number)
        except PageNotAnInteger:
            promotions = paginator.page(1)
        except EmptyPage:
            promotions = paginator.page(paginator.num_pages)

        context["promotions"] = promotions
        return context

    class Meta:
        verbose_name = "Лента акций"
        verbose_name_plural = "Ленты акций"


class PromotionBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        max_length=100, required=True, label="Заголовок секции акций"
    )
    show_count = blocks.IntegerBlock(
        default=3, min_value=1, max_value=12, label="Количество акций для показа"
    )

    class Meta:
        icon = "doc-full"
        label = "Блок акций"

