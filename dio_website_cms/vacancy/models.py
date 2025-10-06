from typing import ClassVar

from django.db import models
from notification.utils import create_admin_notification
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page
from wagtail.search import index


class VacancyPage(Page):
    responsibilities = models.TextField(verbose_name="Обязанности")
    requirements = models.TextField(verbose_name="Требования")
    conditions = models.TextField(verbose_name="Условия")

    content_panels: ClassVar[list] = [
        *Page.content_panels,
        MultiFieldPanel([
            FieldPanel("responsibilities"),
            FieldPanel("requirements"),
            FieldPanel("conditions"),
        ]),
    ]

    search_fields: ClassVar[list] = [
        *Page.search_fields,
        index.SearchField("title"),
    ]

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"


class Vacancy(models.Model):
    title = models.CharField(verbose_name="Вакансия")
    name = models.CharField(verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    resume = models.FileField(
        upload_to="resumes/%Y/%m/%d/",
        verbose_name="Резюме",
        null=True,
        blank=True,
    )
    resume_link = models.URLField(
        verbose_name="Ссылка для скачивания резюме",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_processed = models.BooleanField(default=False, verbose_name="Просмотрено")

    def __str__(self) -> str:
        return f"{self.phone}"

    def save(self, *args, **kwargs) -> None:
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if self.resume:
            self.resume_link = f"http://127.0.0.1:7000/vacancy/resume/download/{self.id}/"  # type: ignore  # noqa: PGH003
        else:
            self.resume_link = "Нет резюме"

        if is_new:
            create_admin_notification(
                title="Новый отзыв на вакансию",
                message=f"Резюме от {self.phone} на вакансию {self.title}",
                url=f"http://127.0.0.1:7000/admin/snippets/vacancy/vacancy/edit/{self.id}/",  # type: ignore  # noqa: PGH003
            )

        super().save(update_fields=["resume_link"])
