import os
import sys

import django


def main():
    try:
        # ... твой код ...
    
        """Создает суперпользователя Django из переменных окружения."""

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip()
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")

    if not all([username, email, password]):
        print("\n" + "="*60, file=sys.stderr)
        print("ОШИБКА: Не заданы переменные окружения для суперюзера", file=sys.stderr)
        print("="*60, file=sys.stderr)
        print("Пожалуйста, укажите в файле .env.prod следующие переменные:", file=sys.stderr)
        print("  - DJANGO_SUPERUSER_USERNAME - логин администратора", file=sys.stderr)
        print("  - DJANGO_SUPERUSER_EMAIL - email администратора", file=sys.stderr)
        print("  - DJANGO_SUPERUSER_PASSWORD - пароль администратора", file=sys.stderr)
        print("="*60 + "\n", file=sys.stderr)
        sys.exit(1)

    if not password.strip():
        print("\n" + "="*60, file=sys.stderr)
        print("ОШИБКА: Пароль не может быть пустым", file=sys.stderr)
        print("="*60 + "\n", file=sys.stderr)
        sys.exit(1)

    # инициализируем Django
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "dio_website_cms.settings.production"
    )
    django.setup()

        from django.contrib.auth import get_user_model
        from django.core.exceptions import ValidationError

        User = get_user_model()

    try:
        if User.objects.filter(username=username).exists():
            print("\n" + "="*60)
            print(f"Суперюзер '{username}' уже существует")
            print("="*60 + "\n")
        else:
            User.objects.create_superuser(
                username=username, email=email, password=password
            )
            print("\n" + "="*60)
            print(f"Суперюзер '{username}' успешно создан")
            print("="*60 + "\n")

    except ValidationError as e:
        print("\n" + "="*60, file=sys.stderr)
        print(f"ОШИБКА валидации: {e}", file=sys.stderr)
        print("="*60 + "\n", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print("\n" + "="*60, file=sys.stderr)
        print(f"НЕОЖИДАННАЯ ОШИБКА: {e}", file=sys.stderr)
        print("="*60 + "\n", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
