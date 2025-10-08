from typing import ClassVar

from django import forms
from django.db.models import QuerySet
from django.utils.html import format_html
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from .models import AddDocument, UploadDocument


class DocumentViewSet(SnippetViewSet):
    model = AddDocument
    menu_label = "Добавленые документы"
    menu_icon = "snippet"
    menu_order = 300
    list_display = ("created_at",)
    list_filter = ("created_at",)
    search_fields = ("page_content", "metadata")
    add_to_admin_menu = False

    panels: ClassVar[list] = [
        MultiFieldPanel(
            [
                FieldPanel("page_content", widget=forms.Textarea(attrs={"rows": 10})),
                FieldPanel("metadata"),
            ],
        )
    ]

    def get_queryset(self, request) -> QuerySet:
        qs = super().get_queryset(request)
        if qs is None:
            qs = AddDocument.objects.all()

        return qs.order_by("-created_at")

    def has_add_permission(self, request) -> bool:  # noqa: ARG002, PLR6301
        return False


class UploadDocumentViewSet(SnippetViewSet):
    model = UploadDocument
    menu_label = "Загруженные документы"
    menu_icon = "upload"
    menu_order = 310
    add_to_admin_menu = False

    list_display = ("created_at",)
    list_filter = ("created_at",)
    search_fields = ("file",)

    panels: ClassVar[list] = [
        FieldPanel("file"),
    ]

    def get_queryset(self, request) -> QuerySet:
        qs = super().get_queryset(request)
        if qs is None:
            qs = UploadDocument.objects.all()

        return qs.order_by("-created_at")

    def file_link(self, obj) -> str:  # noqa: PLR6301
        if obj.file:
            return format_html(
                '<a href="{}" target="_blank" download>📎 {}</a>',
                obj.file.url,
                obj.file.name.split("/")[-1],
            )
        return "— Нет файла —"

    file_link.short_description = "Файл"
    file_link.admin_order_field = "file"

    def has_add_permission(self, request) -> bool:  # noqa: ARG002, PLR6301
        return True

    def has_change_permission(self, request, obj=None) -> bool:  # noqa: ARG002, PLR6301
        return True

    def has_delete_permission(self, request, obj=None) -> bool:  # noqa: ARG002, PLR6301
        return True


class DocumentViewSetGroup(SnippetViewSetGroup):
    menu_label = "AI docs "
    menu_icon = "code"
    menu_order = 300
    items = (DocumentViewSet, UploadDocumentViewSet)


register_snippet(DocumentViewSetGroup)
