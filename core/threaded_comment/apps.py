from django.apps import AppConfig


class ThreadedCommentConfig(AppConfig):
    name = "core.threaded_comment"
    label = "threaded_comment"
    verbose_name = "Threaded Comment"

    def ready(self):
        from . import signals
