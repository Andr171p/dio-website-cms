from .models import AdminNotification


def create_admin_notification(message, level="info", user=None, url=None):
    """Создает новое уведомление в базе данных."""
    return AdminNotification.objects.create(message=message, level=level, user=user, url=url)
