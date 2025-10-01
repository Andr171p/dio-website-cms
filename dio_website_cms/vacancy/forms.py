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
                    "class": "form-control-file",
                    "placeholder": "Резюме",
                    "accept": ".pdf,.doc,.docx,.txt",
                    "id": "resume-input",
                }
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["resume"].widget.attrs.update({"data-display": "file-display"})

    def clean_phone(self) -> str | None:
        phone = self.cleaned_data.get("phone")
        if phone:
            digits = re.sub(r"\D", "", phone)
            if digits.startswith(("7", "8")):
                digits = digits[1:]
            if len(digits) != 10:  # noqa: PLR2004
                raise forms.ValidationError("Номер должен содержать 10 цифр")
            return f"+7 ({digits[:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:10]}"
        return phone

    def save(self, commit=True) -> super:
        return super().save(commit=commit)
