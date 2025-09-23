from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import AdminNotification


class AdminNotificationViewSet(SnippetViewSet):
    model = AdminNotification
    menu_label = "Уведомления"
    menu_icon = "warning"
    list_display = ("message", "level", "user", "created_at", "is_read")
    list_filter = ("level", "is_read", "created_at")
    search_fields = ("message",)


register_snippet(AdminNotificationViewSet)
