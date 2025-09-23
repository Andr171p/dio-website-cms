# forms.py
from typing import ClassVar

from django import forms

from .models import FeedbackMessage


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedbackMessage
        fields: ClassVar[list[str]] = [
            "name",
            "email",
            "phone",
            "company",
            "service_of_interest",
            "message",
        ]
        widgets: ClassVar[dict] = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ваше имя"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Телефон"}),
            "company": forms.TextInput(attrs={"class": "form-control", "placeholder": "Компания"}),
            "service_of_interest": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Интересующа услуга"}
            ),
            "message": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Сообщение", "rows": 4}
            ),
        }
