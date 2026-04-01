"""
Django settings for dio_website_cms project.
"""

import os
import sys
from pathlib import Path

# ===== БАЗОВЫЕ ПУТИ =====
# Устанавливаем BASE_DIR на /app
BASE_DIR = Path('/app')
PROJECT_DIR = BASE_DIR / 'dio_website_cms'

# Quick-start development settings - unsuitable for production
CSRF_USE_SESSIONS = False
CSRF_COOKIE_HTTPONLY = False

# Application definition
INSTALLED_APPS = [
    "home",
    "search",
    "cases",
    "base",
    "news",
    "services",
    "chat",
    # Установленные приложения
    "wagtail.contrib.settings",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    "django_filters",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "wagtail.api.v2",
    "rest_framework",
    "corsheaders",
    'django_htmx',
    "tailwind",
    
    # "wagtailmenus",
    
]

WAGTAILEMBEDS_RESPONSIVE_HTML = True
WAGTAILEMBEDS_FINDERS = [
    {
        "class": "wagtail.embeds.finders.oembed",
        "options": {"timeout": 5},
    }
]

WAGTAILAPI_BASE_URL = "http://localhost:8000/api"
WAGTAILIMAGES_IMAGE_MODEL = "wagtailimages.Image"

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    'django_htmx.middleware.HtmxMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = "dio_website_cms.urls"

# Настройки WhiteNoise
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(PROJECT_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
                # "wagtailmenus.context_processors.wagtailmenus"
            ],
        },
    },
]

WSGI_APPLICATION = "dio_website_cms.wsgi.application"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
}

# ===== DATABASE =====
DB_DIR = BASE_DIR / 'db'
DB_DIR.mkdir(exist_ok=True)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": DB_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "ru-RU"
USE_THOUSAND_SEPARATOR = True
TIME_ZONE = "Asia/Yekaterinburg"
USE_TZ = True
THOUSAND_SEPARATOR = " "
DECIMAL_SEPARATOR = ","

# ===== STATIC & MEDIA - УПРОЩЕННАЯ ВЕРСИЯ =====
# Используем абсолютные пути для надежности
STATIC_URL = '/static/'
STATIC_ROOT = '/app/static'  # фиксированный абсолютный путь

MEDIA_URL = '/media/'
MEDIA_ROOT = '/app/media'

# НЕ ИСПОЛЬЗУЕМ STATICFILES_DIRS, чтобы избежать конфликтов
STATICFILES_DIRS = []

# Создаем директории
os.makedirs(STATIC_ROOT, exist_ok=True)
os.makedirs(MEDIA_ROOT, exist_ok=True)

# Default storage settings
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10_000

# Wagtail image settings
WAGTAILIMAGES_MAX_UPLOAD_SIZE = 20 * 1024 * 1024
WAGTAILIMAGES_JPEG_QUALITY = 95
WAGTAILIMAGES_WEBP_QUALITY = 95
WAGTAILIMAGES_PNG_QUALITY = 95
WAGTAILIMAGES_OPTIMIZE_IMAGES = False

# Wagtail settings
WAGTAIL_SITE_NAME = "dio_website_cms"
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}
WAGTAILADMIN_BASE_URL = "http://example.com"
WAGTAILDOCS_EXTENSIONS = ["csv", "docx", "key", "odt", "pdf", "pptx", "rtf", "txt", "xlsx", "zip"]

# Email settings
MAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").strip().lower() == "true"
EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL", "False").strip().lower() == "true"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = os.environ.get("SERVER_EMAIL")
FASTAPI_RAG = os.environ.get("FASTAPI_RAG")
SITE_DOMAIN = os.environ.get("SITE_DOMAIN")
