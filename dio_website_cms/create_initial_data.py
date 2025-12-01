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

    print("=" * 50)
    print("DEBUG: Проверка состояния базы данных")
    print("=" * 50)
    
    sites_count = Site.objects.count()
    print(f"Всего Site в БД: {sites_count}")
    
    home_pages = HomePage.objects.all()
    print(f"Всего HomePage: {home_pages.count()}")
    for hp in home_pages:
        print(f"  - ID {hp.id}: {hp.title} (slug: {hp.slug})")
    
    # Ищем Site с is_default_site=True
    default_site = Site.objects.filter(is_default_site=True).first()
    if default_site:
        print(f"Найден default Site: ID={default_site.id}, hostname={default_site.hostname}")
        print(f"Root page: {default_site.root_page.title if default_site.root_page else 'Нет'}")
    else:
        print("Default Site не найден, создаем...")
        
        root = Page.get_first_root_node()
        
        if not Page.objects.filter(slug="home").exists():
            home = HomePage(title="Главная", slug="home")
            root.add_child(instance=home)
            home.save_revision().publish()
            print("✓ HomePage создана")
        else:
            home = HomePage.objects.first()
            print(f"✓ HomePage уже существует: {home.title}")
        
        site_domain = os.environ.get("SITE_DOMAIN", "localhost")
        
        Site.objects.create(
            hostname=site_domain,
            port=int(os.environ.get("SITE_PORT", 80)),
            site_name=os.environ.get("SITE_NAME", "DIO Website"),
            root_page=home,
            is_default_site=True,
        )
        print(f"✓ Site создан: {site_domain} -> {home.title}")
    
    print("=" * 50)
    print("Initial data check completed")
    print("=" * 50)

except Exception as e:
    print(f"Ошибка при создании initial data: {e}")
    import traceback
    traceback.print_exc()