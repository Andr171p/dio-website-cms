# home/apps.py
from django.apps import AppConfig
from django.db import DatabaseError  # ловим всё, что связано с БД


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self):
        # Импортируем здесь, чтобы избежать циклических импортов
        from wagtail.models import Site
        from .models import HomePage

        # Если база ещё не готова (миграции не выполнены) — просто выходим
        try:
            site = Site.objects.first()
        except DatabaseError:
            return  # миграции ещё не прошли — ничего не делаем

        if not site:
            return

        # Если root_page ещё не установлен или неправильный — исправляем
        if not hasattr(site.root_page, 'specific_class') or \
           site.root_page.specific_class != HomePage:

            home_page = HomePage.objects.first()
            if not home_page:
                # Создаём минимальную домашнюю страницу, если вообще ничего нет
                home_page = HomePage(title="Home", slug="home", body=[])
                # Нужно добавить в дерево Wagtail
                from wagtail.models import Page
                Page.get_first_root_node().add_child(instance=home_page)

            site.root_page = home_page
            site.save(update_fields=['root_page'])