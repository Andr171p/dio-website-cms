from typing import ClassVar

import os

from django.db.models import QuerySet
from django.http import FileResponse, HttpResponse
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
    list_display = ("title", "created_at", "is_processed")
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
                FieldPanel("resume_link", read_only=True),
            ],
            heading="Информация о кандидате",
        ),
        FieldPanel("is_processed"),
    ]

    def get_queryset(self, request) -> QuerySet:
        qs = super().get_queryset(request)
        if qs is None:
            qs = Vacancy.objects.all()

        return qs.order_by("-created_at")

    def has_add_permission(self, request) -> bool:  # noqa: ARG002, PLR6301
        return False


def download_resume(request, vacancy_id) -> FileResponse | HttpResponse:  # noqa: ARG001
    try:
        vacancy = Vacancy.objects.get(id=vacancy_id)
        if not vacancy.resume:
            return HttpResponse("Файл не найден", status=404)

        file_path = vacancy.resume.path
        if not os.path.exists(file_path):
            return HttpResponse("Файл не найден на сервере", status=404)

        file = open(file_path, "rb")  # noqa: SIM115
        response = FileResponse(file, content_type="application/octet-stream")
        response["Content-Disposition"] = (
            f'attachment; filename="{os.path.basename(vacancy.resume.name) or "resume"}"'
        )
        response["Content-Length"] = os.path.getsize(file_path)
        return response  # noqa: TRY300
    except Vacancy.DoesNotExist:
        return HttpResponse("Вакансия не найдена", status=404)
    except (ValueError, OSError):
        return HttpResponse("Ошибка при загрузке файла", status=500)


register_snippet(VacancyViewSet)
