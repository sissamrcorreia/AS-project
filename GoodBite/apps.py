from django.apps import AppConfig

class GoodBiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'GoodBite'

    def ready(self):
        import GoodBite.signals