FROM python:3.12-slim-bookworm
# Add user that will be used in the container.
RUN useradd wagtail

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
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
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# СОЗДАЙТЕ ПАПКИ И ДАЙТЕ ПРАВА
RUN mkdir -p /app/static /app/media && chown -R wagtail:wagtail /app/static /app/media

# Set this directory to be owned by the "wagtail" user.
RUN chown wagtail:wagtail /app

# Copy the source code of the project into the container.
COPY --chown=wagtail:wagtail . .

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

CMD sh -c "cd /app/dio_website_cms && \
    python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput --clear && \
    exec gunicorn dio_website_cms.wsgi:application --bind 0.0.0.0:8000"