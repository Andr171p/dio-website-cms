from django.urls import path
from . import views

app_name = 'programs'

urlpatterns = [
    path('search/<int:page_id>/', views.search_products, name='search_products'),
]