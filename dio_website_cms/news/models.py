from django.db import models
from wagtail.models import Page


class NewsPage(Page):
    """Новостная страница"""
    publish_date = models.DateField(auto_now_add=True, verbose_name="Дата публикации")
    headline = models.CharField(blank=True, verbose_name="Новостной заголовок ")
