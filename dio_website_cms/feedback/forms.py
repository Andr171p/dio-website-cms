# forms.py
from typing import ClassVar

from django import forms

from .models import FeedbackMessage


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedbackMessage
        fields: ClassVar[list[str]] = ["name", "email", "phone", "message"]
        widgets: ClassVar[dict] = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ваше имя"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Ваш email"}),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ваш телефон"}
            ),
            "message": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Ваше сообщение", "rows": 4}
            ),
        }
