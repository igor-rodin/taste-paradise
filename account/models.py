from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, verbose_name="Пользователь", on_delete=models.CASCADE
    )
    avatar = models.ImageField(
        upload_to="images/avatars/",
        default="images/avatars/profile.svg",
    )
    archived = models.BooleanField(default=False, verbose_name="Архивирован")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"
        ordering = ["-created"]
        indexes = [models.Index(fields=["-created"])]
