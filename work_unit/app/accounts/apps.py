from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.accounts"


default_app_config = 'accounts.apps.AccountsConfig'
