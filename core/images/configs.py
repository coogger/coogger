from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class DefaultConfig(dict):
    folder_name = "images/"
    upload_url = "coogger-images/"
    upload_url_name = "coogger-images"
    max_size = 4

    @classmethod
    def update(cls, d):
        for key, value in d.items():
            setattr(cls, key, value)


configs = getattr(settings, "images", None)
if configs:
    if isinstance(configs, dict):
        DefaultConfig.update(configs)
    else:
        raise ImproperlyConfigured("images setting must be a dictionary type.")
