from django import template

from .models import AdminNotification

register = template.Library()


@register.simple_tag(takes_context=True)
def get_unread_notifications(context, user):
    # Можно добавить логику, например, показывать только последние 5
    return AdminNotification.objects.filter(is_read=False, user=user)
