from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = 'apps.users'

    def ready(self):
        from . import signals
