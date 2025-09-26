from chat import views as chat_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from feedback import views as feedback_views
from search import views as search_views
from vacancy import views as vacancies_views
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("settings/", include("wagtail.contrib.settings.urls")),
    path("chat/", chat_views.chat, name="chat"),
    path("documents/add/", chat_views.add_document_, name="add document"),
    path("documents/upload/", chat_views.upload_document_, name="upload document"),
    path("documents/delete/", chat_views.delete_document_, name="delete document"),
    path("feedback/", feedback_views.feedback_view, name="feedback"),
    path("vacancy/", vacancies_views.vacancy_view, name="vacancy"),
    path("", include("wagtail.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Добавляем маршруты для статических и медиафайлов в режиме DEBUG
if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path("", include(wagtail_urls)),
]
