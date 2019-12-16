from django.forms import CharField

from .widgets import EditorMdWidget


class EditorMdFormField(CharField):
    def __init__(self, *args, **kwargs):
        super(EditorMdFormField, self).__init__(*args, **kwargs)
        self.widget = EditorMdWidget()
