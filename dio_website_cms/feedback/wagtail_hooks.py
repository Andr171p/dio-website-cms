# wagtail_hooks.py
from django.contrib import admin

from .models import FeedbackMessage


@admin.register(FeedbackMessage)
class FeedbackMessageAdmin(admin.ModelAdmin):
    model = FeedbackMessage
    menu_label = "Обратная связь"
    menu_icon = "mail"
    list_display = (
        "name",
        "email",
        "phone",
        "company",
        "service_of_interest",
        "message",
        "created_at",
        "is_processed",
    )
    list_filter = ("created_at", "is_processed")
    search_fields = ("name", "email", "message")
    list_editable = ("is_processed",)

    def has_add_permission(self, request):  # noqa: ARG002, PLR6301
        return False

    # Разрешаем только изменение поля is_processed
    def get_readonly_fields(self, request, obj=None):  # noqa: ARG002
        if obj:  # editing an existing object
            return [
                "name",
                "email",
                "phone",
                "company",
                "service_of_interest",
                "message",
                "created_at",
            ]
        return self.readonly_fields
