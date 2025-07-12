from django.apps import AppConfig


class LoginConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    
    def ready(self):
        import apps.accounts.signals
