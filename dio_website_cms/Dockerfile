FROM python:3.12-slim-bookworm

EXPOSE 8000
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=dio_website_cms.settings.production

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

RUN pip install --no-cache-dir "gunicorn==20.0.4" python-dotenv

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# НЕ создаем БД здесь - Django сделает это при migrate
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]