from typing import ClassVar

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import Vacancy


class VacancyViewSet(SnippetViewSet):
    model = Vacancy
    menu_label = "Отзывы на вакансии"
    menu_icon = "table"
    menu_order = 300
    add_to_settings_menu = False
    list_display = ("title", "name", "phone", "created_at", "is_processed")
    list_filter = ("created_at", "is_processed")
    search_fields = ("title", "name", "phone")
    add_to_admin_menu = True

    panels: ClassVar[list] = [
        MultiFieldPanel(
            [
                FieldPanel("title", read_only=True),
                FieldPanel("name", read_only=True),
                FieldPanel("phone", read_only=True),
                FieldPanel("created_at", read_only=True),
            ],
            heading="Информация о кандидате",
        ),
        MultiFieldPanel(
            [
                FieldPanel("resume", read_only=True),
            ],
        ),
        FieldPanel("is_processed"),
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if qs is None:
            qs = Vacancy.objects.all()

        return qs.order_by("-created_at")

    def has_add_permission(self, request):  # noqa: ARG002, PLR6301
        return False


register_snippet(VacancyViewSet)
