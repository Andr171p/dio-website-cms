import logging

from admin_email.models import AdminEmail
from dio_website_cms.settings.dev import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


def send_admin_notification(notification_instance) -> None:
    try:
        context = {
            "title": notification_instance.title,
            "message": notification_instance.message,
            "url": notification_instance.url,
            "created_at": notification_instance.created_at,
            "notification": notification_instance,
        }

        # Получаем email администратора из настроек
        admin_emails = list(AdminEmail.objects.values_list("email", flat=True))

        if not admin_emails:
            logger.warning("Нет ни одного email администратора для отправки уведомлений")
            return

        subject = f"Уведомление: {notification_instance.title}"

        html_message = render_to_string("emails/admin_notification.html", context)
        text_message = strip_tags(html_message)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            from_email=EMAIL_HOST_USER,
            to=admin_emails,
        )
        email.attach_alternative(html_message, "text/html")

        result = email.send(fail_silently=False)
        logger.info("Admin notification email sent. Result: %s", result)

    except Exception as e:  # noqa: BLE001
        logger.error(f"Failed to send admin notification email: {e!s}")  # noqa: G004, TRY400
