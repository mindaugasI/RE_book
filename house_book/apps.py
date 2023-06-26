from django.apps import AppConfig


class HouseBookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'house_book'

    def ready(self):
        from .signals import create_profile, save_profile
