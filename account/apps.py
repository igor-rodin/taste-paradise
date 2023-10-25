from django.apps import AppConfig


class AccountConfig(AppConfig):
    verbose_name = "Профиль пользователя"
    default_auto_field = "django.db.models.BigAutoField"
    name = "account"
