# forms.py
from typing import ClassVar

import re

from django import forms
from django.core.validators import validate_email

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
                attrs={"class": "form-control", "placeholder": "Интересующая услуга"}
            ),
            "message": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Сообщение", "rows": 4}
            ),
        }

    def clean_email(self):
        """Валидация email"""
        email = self.cleaned_data.get("email")

        if email:
            # Базовая проверка формата
            try:
                validate_email(email)
            except forms.ValidationError:
                raise forms.ValidationError("Введите корректный email адрес") from None
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone:
            # Удаляем все нецифровые символы
            digits = re.sub(r"\D", "", phone)

            # Проверяем российские номера
            if digits.startswith("7") or digits.startswith("8"):  # noqa: PIE810
                digits = digits[1:]

            if len(digits) != 10:  # noqa: PLR2004
                raise forms.ValidationError("Номер должен содержать 10 цифр")

            # Форматируем номер
            return f"+7 ({digits[:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:10]}"

        return phone
