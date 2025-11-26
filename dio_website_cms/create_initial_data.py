# dio_website_cms/create_initial_data.py
import os
import django
from django.core.exceptions import ObjectDoesNotExist

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dio_website_cms.settings.production')
django.setup()

from wagtail.models import Site, Page
from home.models import HomePage
try:
    # ... твой код ...

    if not Site.objects.filter(is_default_site=True).exists():
        root = Page.get_first_root_node()
        if not Page.objects.filter(slug='home').exists():
            home = HomePage(title="Главная", slug="home")
            root.add_child(instance=home)
            print("HomePage создана")

        Site.objects.create(
            hostname="localhost",
            port=8000,
            site_name="DIO Website",
            root_page=HomePage.objects.first(),
            is_default_site=True
        )
        print("Site создан")
    else:
        print("Site уже существует")
except django.db.utils.OperationalError as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Info: {e}")