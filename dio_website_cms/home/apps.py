from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "home"

    def ready(self):
        pass


# class HomeConfig(AppConfig):
#     default_auto_field = "django.db.models.BigAutoField"
#     name = "home"

#     def ready(self):
#         from wagtail.models import Site

#         from .models import HomePage

#         site = Site.objects.first()
#         if site and not site.root_page.specific_class == HomePage:
#             site.root_page = HomePage.objects.first() or HomePage(title="Home")
#             site.save()
