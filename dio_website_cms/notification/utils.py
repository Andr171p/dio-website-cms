from .models import AdminNotification


def create_admin_notification(message, url=None):
    """Создает новое уведомление в базе данных."""
    return AdminNotification.objects.create(message=message, url=url)
