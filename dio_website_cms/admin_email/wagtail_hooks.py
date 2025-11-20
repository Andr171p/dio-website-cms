from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import AdminEmail


class AdminEmailModelAdmin(SnippetViewSet):
    model = AdminEmail
    menu_label = "Администраторы"
    menu_icon = "user"  # иконка в меню
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    add_to_admin_menu = True

    list_display = ("email", "fio", "created_at")
    search_fields = ("email", "fio")


register_snippet(AdminEmailModelAdmin)
