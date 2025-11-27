# dio_website_cms/create_initial_data.py
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dio_website_cms.settings.production")
django.setup()

from home.models import HomePage
from wagtail.models import Page, Site

if not Site.objects.filter(is_default_site=True).exists():
    root = Page.get_first_root_node()
    if not Page.objects.filter(slug="home").exists():
        home = HomePage(title="Главная", slug="home")
        root.add_child(instance=home)
        print("HomePage создана")

    Site.objects.create(
        hostname="localhost",
        port=8000,
        site_name="DIO Website",
        root_page=HomePage.objects.first(),
        is_default_site=True,
    )
    print("Site создан")
else:
    print("Site уже существует")
