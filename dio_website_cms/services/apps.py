# dio_website_cms/services/apps.py
from django.apps import AppConfig

class ServicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'services'

    def ready(self):
        # Убедитесь, что здесь нет запросов к базе данных
        pass  # Или перенесите логику в представления