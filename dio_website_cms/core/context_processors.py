from django.core.cache import cache
from django.http import HttpRequest

from .models import NavigationMenuSettings, SiteSettings

TTL = 3600


def navigation_menu_context(request: HttpRequest) -> dict[str, NavigationMenuSettings | None]:
    """Добавляет навигационное меню в контекст всех страниц"""
    if not hasattr(request, "site") or request.site is None:
        return {"navigation_menu": None}
    cache_key = f"navigation_menu_{request.site.id}"
    navigation_menu = cache.get(cache_key)
    if not navigation_menu:
        try:
            navigation_menu = NavigationMenuSettings.for_site(request.site)
            cache.set(cache_key, navigation_menu, TTL)
        except (NavigationMenuSettings.DoesNotExist, AttributeError, Exception):
            navigation_menu = None
    return {"navigation_menu": navigation_menu}


def site_settings_context(request: HttpRequest) -> dict[str, SiteSettings | None]:
    """Добавляет настройки сайта на все страницы"""
    if not hasattr(request, "site") or request.site is None:
        return {"site_settings": None}
    cache_key: str = f"site_settings_{request.site.id}"
    site_settings = cache.get(cache_key)
    if not site_settings:
        try:
            site_settings = SiteSettings.for_site(request.site)
            cache.set(cache_key, site_settings, TTL)
        except (SiteSettings.DoesNotExist, AttributeError, Exception):
            site_settings = None
    return {"site_settings": site_settings}
