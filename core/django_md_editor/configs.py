from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

DEFAULT_CONFIG = {
    "width": "100%",
    "heigth": "500px",
    "toolbar": [
        "undo",
        "redo",
        "|",
        "bold",
        "del",
        "italic",
        "quote",
        "ucwords",
        "uppercase",
        "lowercase",
        "|",
        "h1",
        "h2",
        "h3",
        "h5",
        "h6",
        "|",
        "list-ul",
        "list-ol",
        "hr",
        "|",
        "link",
        "reference-link",
        "image",
        "code",
        "preformatted-text",
        "code-block",
        "table",
        "datetime",
        "emoji",
        "html-entities",
        "pagebreak",
        "goto-line",
        "|",
        "help",
        "info",
        "||",
        "preview",
        "watch",
        "fullscreen",
    ],
    "upload_image_formats": [
        "jpg",
        "JPG",
        "jpeg",
        "JPEG",
        "gif",
        "GIF",
        "png",
        "PNG",
        "bmp",
        "BMP",
        "webp",
        "WEBP",
    ],
    "image_floder": "editor",
    "theme": "default",
    "preview_theme": "default",
    "editor_theme": "default",
    "html_decode": "html, iframe",
    "at_link_base": "/@",
    "image_upload_url": "/media/uploads/",
    "toolbar_autofixed": False,
    "search_replace": False,
    "emoji": False,
    "tex": True,
    "image_upload": False,
    "flow_chart": True,
    "sequence": True,
    "at_link": False,
    "email_link": False,
}


class DictToObject(object):
    def __init__(self, d):
        for key, value in d.items():
            if isinstance(value, (list, tuple)):
                setattr(
                    self,
                    key,
                    [DictToObject(x) if isinstance(x, dict) else x for x in value],
                )
            else:
                setattr(
                    self, key, DictToObject(value) if isinstance(value, dict) else value
                )


default_config = DictToObject(DEFAULT_CONFIG).__dict__
configs = getattr(settings, "MDEDITOR_CONFIGS", None)
if configs:
    if isinstance(configs, dict):
        default_config.update(configs)
    else:
        raise ImproperlyConfigured(
            "MDEDITOR_CONFIGS setting must be a\
                        dictionary type."
        )
