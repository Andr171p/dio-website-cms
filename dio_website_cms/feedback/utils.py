import pytz  # Для работы с конкретными часовыми поясами
from django.utils import timezone


def get_tumen_time():
    yekaterinburg_tz = pytz.timezone("Asia/Yekaterinburg")

    now = timezone.now()

    return now.astimezone(yekaterinburg_tz)
