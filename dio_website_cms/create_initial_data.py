# dio_website_cms/create_initial_data.py
import os
import sys

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dio_website_cms.settings.production")

try:
    django.setup()
except Exception as e:
    print(f"Ошибка инициализации Django: {e}")
    sys.exit(0)

try:
    from django.db import connection
    from home.models import HomePage
    from wagtail.models import Page, Site

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='wagtailcore_site'"
        )
        if not cursor.fetchone():
            print("Таблицы еще не созданы, пропускаем создание initial data")
            sys.exit(0)

    if not Site.objects.filter(is_default_site=True).exists():
        root = Page.get_first_root_node()
        if not Page.objects.filter(slug="home").exists():
            home = HomePage(title="Главная", slug="home")
            root.add_child(instance=home)
            home.save_revision().publish()
            print("HomePage создана")

        site_domain = os.environ.get("SITE_DOMAIN")

        Site.objects.create(
            hostname=site_domain,
            port=int(os.environ.get("SITE_PORT", 80)),
            site_name=os.environ.get("SITE_NAME"),
            root_page=HomePage.objects.first(),
            is_default_site=True,
        )
        print("Site создан")
    else:
        print("Site уже существует")

except Exception as e:
    print(f"Ошибка при создании initial data: {e}")
