from django.apps import AppConfig


class CooggerappConfig(AppConfig):
    name = "core.cooggerapp"
    label = "cooggerapp"
    verbose_name = "Main application"

    def ready(self):
        from . import signals
