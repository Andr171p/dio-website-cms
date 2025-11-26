#!/bin/sh
set -e

echo "=== DIO Wagtail — запуск ==="

# Создаем базу данных если её нет
if [ ! -f /app/db.sqlite3 ]; then
    echo "Создаём базу данных..."
    python -c "
import sqlite3
conn = sqlite3.connect('/app/db.sqlite3')
conn.close()
print('База данных создана')
"
fi

echo "Запускаем миграции..."
python manage.py migrate --noinput

echo "Собираем статику..."
python manage.py collectstatic --noinput

echo "Создаём суперюзера..."
python create_superuser.py 2>/dev/null || echo "Суперюзер уже есть"

echo "Создаём Site и HomePage..."
python create_initial_data.py 2>/dev/null || echo "Site уже создан"

echo "======================================="
echo "WAGTAIL ГОТОВ! Открывай http://localhost:8000"
echo "======================================="

exec gunicorn dio_website_cms.wsgi:application --bind 0.0.0.0:8000 --workers 2 --access-logfile - --error-logfile -