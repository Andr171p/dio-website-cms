# yourapp/models.py
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import messages
from wagtail.models import Page
from wagtail.admin.models import Message
from django.contrib.auth.models import User
from .forms import ContactForm
from .models import ContactSettings, ContactSubmission
from django.conf import settings

class HomePage(Page):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # Добавляем форму и настройки в контекст
        context['form'] = ContactForm(request.POST or None)
        context['contact_settings'] = ContactSettings.for_request(request)
        return context

    def serve(self, request):
        context = self.get_context(request)
        form = context['form']
        contact_settings = context['contact_settings']

        if request.method == "POST" and form.is_valid():
            # Сохраняем заявку
            submission = ContactSubmission(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data["phone"],
                message=form.cleaned_data["message"],
            )
            submission.save()

            # Отправляем email
            recipient_email = contact_settings.form_recipient_email
            if recipient_email:
                subject = f"Новая заявка от {form.cleaned_data['name']}"
                message = (
                    f"Имя: {form.cleaned_data['name']}\n"
                    f"Email: {form.cleaned_data['email']}\n"
                    f"Телефон: {form.cleaned_data['phone'] or 'Не указан'}\n"
                    f"Сообщение: {form.cleaned_data['message'] or 'Не указано'}"
                )
                try:
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[recipient_email],
                        fail_silently=False,
                    )
                    messages.success(request, "Ваша заявка успешно отправлена!")
                except Exception as e:
                    messages.error(request, f"Ошибка при отправке: {str(e)}")
            else:
                messages.error(request, "Ошибка: email для заявок не настроен.")

            # Создаем уведомление в админке Wagtail
            notification_message = (
                f"Новая заявка:\n"
                f"Имя: {form.cleaned_data['name']}\n"
                f"Email: {form.cleaned_data['email']}\n"
                f"Телефон: {form.cleaned_data['phone'] or 'Не указан'}\n"
                f"Сообщение: {form.cleaned_data['message'] or 'Не указано'}\n"
                f"Посмотреть: {request.build_absolute_uri('/admin/yourapp/contactsubmission/' + str(submission.id) + '/')}"
            )
            users = contact_settings.notification_users.all() or User.objects.filter(is_staff=True)
            for user in users:
                Message.objects.create(
                    user=user,
                    text=notification_message,
                    level=25,  # Уровень INFO
                )

            return redirect(self.url)

        return super().serve(request)