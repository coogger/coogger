from django.db.models import TextField

from .fields import EditorMdFormField


class EditorMdField(TextField):
    def formfield(self, **kwargs):
        defaults = {"form_class": EditorMdFormField}
        defaults.update(kwargs)
        return super(EditorMdField, self).formfield(**defaults)
