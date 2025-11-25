FROM python:3.12-slim-bookworm
RUN useradd wagtail
EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    DJANGO_SETTINGS_MODULE=dio_website_cms.settings.production

# Install system packages
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

# Install the application server.
RUN pip install "gunicorn==20.0.4"

# Install the project requirements.
COPY dio_website_cms/requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app

RUN mkdir -p /app/static /app/media && chown -R wagtail:wagtail /app/static /app/media
RUN chown wagtail:wagtail /app

# Копируем ТОЛЬКО папку dio_website_cms в /app
COPY --chown=wagtail:wagtail dio_website_cms/ .

USER wagtail

# Теперь manage.py в /app/ (а не в /app/dio_website_cms/)
CMD sh -c "python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput --clear && \
    python create_superuser.py && \
    exec gunicorn dio_website_cms.wsgi:application --bind 0.0.0.0:8000"