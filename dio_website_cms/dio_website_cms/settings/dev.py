from .base import *

# -------------------------------
# РАЗРАБОТКА — локальный запуск
# -------------------------------

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]", "*"]

# Секретный ключ можно захардкодить локально (или оставить через .env)
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-lokal-dev-key-for-runserver")

# Отправка писем в консоль
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# === УБИРАЕМ ТО, ЧТО МЕШАЕТ ЛОКАЛЬНО ===

# 1. Убираем WhiteNoise из middleware (он нужен только в проде)
MIDDLEWARE = [
    m for m in MIDDLEWARE 
    if m != "whitenoise.middleware.WhiteNoiseMiddleware"
]

# 2. Отключаем ManifestStaticFilesStorage (он ломается без collectstatic)
if "ManifestStaticFilesStorage" in str(STORAGES["staticfiles"]):
    STORAGES["staticfiles"]["BACKEND"] = "django.contrib.staticfiles.storage.StaticFilesStorage"

# 3. Подключаем локальные переопределения (если есть .local.py)
try:
    from .local import *
except ImportError:
    pass