from django import template
from wagtail.models import Page, Site

from ..models import NavigationMenu

register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_root(context: dict[str, object]) -> Page:
    """Получает корневую страницу сайта"""
    return Site.find_for_request(context["request"]).root_page


@register.inclusion_tag("base/navigation_menu.html", takes_context=True)
def navigation_menu(
        context: dict[str, object], menu_title: str = "Навигационное меню"
) -> dict[str, object | None]:
    """Получение навигационного меню"""
    try:
        menu = NavigationMenu.objects.get(title=menu_title)
        request = context.get("request")
    except NavigationMenu.DoesNotExist:
        return {"menu_items": None}
    else:
        return {"menu_items": menu.menu_items, "request": request}
