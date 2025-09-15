from django import forms
from wagtail.contrib.forms.forms import BaseForm


class FeedbackForm(BaseForm):
    """Форма обратной связи"""
    name = forms.CharField(
        max_length=100,
        label="Ваше имя",
        widget=forms.TextInput(attrs={"placeholder": "Иван Иванов"})
    )
    phone = forms.CharField(
        max_length=20,
        label="Телефон",
        widget=forms.TextInput(attrs={"placeholder": "+7 (999) 999-99-99"}),
    )
    email = forms.EmailField(
        label="Электронная почта",
        widget=forms.TextInput(attrs={"placeholder": "example@mail.ru"}),
    )
    message = forms.CharField(
        label="Комментарий",
        widget=forms.Textarea(attrs={"rows": 5, "placeholder": "Комментарий"}),
    )
    agreement = forms.BooleanField(
        label="Я согласен на обработку персональных данных", required=True
    )
