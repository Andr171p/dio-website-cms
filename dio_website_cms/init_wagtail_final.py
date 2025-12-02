import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dio_website_cms.settings.production")

import django
django.setup()

print("=== Инициализация Wagtail ===")

SITE_DOMAIN = os.environ.get("SITE_DOMAIN", "localhost")
SITE_NAME = os.environ.get("SITE_NAME", "DIO Website")
SITE_PORT = int(os.environ.get("SITE_PORT", "80"))

print(f"Настройки сайта: {SITE_DOMAIN}:{SITE_PORT} - {SITE_NAME}")

from django.core.management import call_command
from django.db import connection

print("1. Создаю миграции для приложений...")
try:
    call_command('makemigrations', '--noinput')
    print("Миграции созданы")
except Exception as e:
    print(f"Ошибка при создании миграций: {e}")

print("2. Применяю миграции...")
call_command('migrate', '--noinput')

print("3. Проверяю таблицы...")
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='home_homepage'")
        if not cursor.fetchone():
            print("Таблица home_homepage не существует, создаю...")
            call_command('migrate', 'home', '--noinput')
except Exception as e:
    print(f"Ошибка при проверке таблиц: {e}")

print("4. Создаю структуру сайта...")
try:
    from wagtail.models import Page, Site
    from home.models import HomePage
    
    if HomePage.objects.filter(slug='home').exists():
        home = HomePage.objects.get(slug='home')
        print(f"HomePage уже существует: {home.title}")
    else:
        print("Создаю HomePage...")
        
        Page.objects.filter(title__icontains='welcome').delete()
        
        root = Page.objects.get(depth=1)
        home = HomePage(title="Главная", slug="home", live=True)
        root.add_child(instance=home)
        home.save_revision().publish()
        print(f"HomePage создана: {home.id}")
    
    print("5. Настраиваю сайты...")
    
    Site.objects.update_or_create(
        hostname=SITE_DOMAIN,
        defaults={
            'port': SITE_PORT,
            'site_name': SITE_NAME,
            'root_page': home,
            'is_default_site': True,
        }
    )
    
    Site.objects.update_or_create(
        hostname='localhost',
        defaults={
            'port': 8000,
            'site_name': f'{SITE_NAME} (Local)',
            'root_page': home,
            'is_default_site': False,
        }
    )
    
    Site.objects.update_or_create(
        hostname='127.0.0.1',
        defaults={
            'port': 8000,
            'site_name': f'{SITE_NAME} (Local IP)',
            'root_page': home,
            'is_default_site': False,
        }
    )
    
    print("Сайты настроены:")
    print(f"  - {SITE_DOMAIN}:{SITE_PORT} (основной)")
    print(f"  - localhost:8000 (для разработки)")
    print(f"  - 127.0.0.1:8000 (альтернатива)")
    
except Exception as e:
    print(f"Ошибка при создании структуры: {e}")
    import traceback
    traceback.print_exc()

print("=== Инициализация завершена ===")