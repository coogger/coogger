from django.apps import AppConfig

class CooggerappConfig(AppConfig):
    name = 'cooggerapp'

    def ready(self):
        from . import signals