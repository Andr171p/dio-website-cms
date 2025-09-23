<<<<<<< HEAD
from chat import views
=======
# from casestudies.api import router as cases_router
>>>>>>> b17fa042fdb595f90e37f79bb887188aa444b013
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from search import views as search_views
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("settings/", include("wagtail.contrib.settings.urls")),
<<<<<<< HEAD
    path("chat/", views.chat, name="chat"),
    path("documents/add/", views.add_document_, name="add document"),
    path("documents/upload/", views.upload_document_, name="upload document"),
    path("documents/delete/", views.delete_document_, name="delete document"),
    path("", include("wagtail.urls")),
=======
>>>>>>> b17fa042fdb595f90e37f79bb887188aa444b013
]

# Добавляем маршруты для статических и медиафайлов в режиме DEBUG
if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path("", include(wagtail_urls)),
]