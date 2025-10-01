import os  # noqa: INP001

import pytz
from django.core.exceptions import ValidationError
from django.utils import timezone


def get_tumen_time():
    yekaterinburg_tz = pytz.timezone("Asia/Yekaterinburg")

    now = timezone.now()

    return now.astimezone(yekaterinburg_tz)


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".pdf", ".doc", ".docx", ".txt"]
    if ext.lower() not in valid_extensions:
        raise ValidationError("Поддерживаются только файлы PDF, DOC, DOCX и TXT")
