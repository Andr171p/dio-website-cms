from django.db import models

# Create your models here.

# Create your models here.

# Create your models here.


class AdminEmail(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email администратора")
    fio = models.CharField(verbose_name="ФИО администратора", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Администратор"
        verbose_name_plural = "Администраторы"
