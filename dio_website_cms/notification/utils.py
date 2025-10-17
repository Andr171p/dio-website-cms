from django.core.mail import send_mail

from .models import AdminNotification


def create_admin_notification(title, message, url=None) -> AdminNotification:
    """Создает новое уведомление в базе данных."""
    return AdminNotification.objects.create(title=title, message=message, url=url)


def send_notification(title: str):
    send_mail(
        subject=title,
        message="",
        recipient_list=["medvedevdelovoy@gmail.com"],
        from_email="",
    )
