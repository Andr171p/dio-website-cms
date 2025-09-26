from typing import ClassVar

import re

from django import forms

from .models import Vacancy


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields: ClassVar[list[str]] = [
            "title",
            "name",
            "phone",
            "resume",
        ]
        widgets: ClassVar[dict] = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Вакансия"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ваше имя"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Телефон"}),
            "resume": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Резюме",
                    "accept": ".pdf,.doc,.docx,.txt",
                }
            ),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone:
            # Удаляем все нецифровые символы
            digits = re.sub(r"\D", "", phone)

            # Проверяем российские номера
            if digits.startswith("7") or digits.startswith("8"):
                digits = digits[1:]

            if len(digits) != 10:
                raise forms.ValidationError("Номер должен содержать 10 цифр")

            # Форматируем номер
            return f"+7 ({digits[:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:10]}"

        return phone
