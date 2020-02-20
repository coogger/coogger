from django import forms
from django.contrib.admin.widgets import AdminTextareaWidget
from django.forms import Textarea
from django.forms.utils import flatatt
from django.template.loader import render_to_string
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from core.md_editor.configs import default_config

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text


class EditorMdWidget(Textarea):
    def __init__(self, attrs=None):
        super(EditorMdWidget, self).__init__(attrs)

    def build_attrs(self, base_attrs, extra_attrs=None, **kwargs):
        attrs = dict(base_attrs, **kwargs)
        if extra_attrs:
            attrs.update(extra_attrs)
        return attrs

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ""
        final_attrs = self.build_attrs(self.attrs, attrs, name=name)
        context = dict(
            attrs=flatatt(final_attrs),
            markdown=conditional_escape(force_text(value)),
            id=attrs["id"],
            config=default_config,
        )
        return mark_safe(render_to_string("form.html", context))

    @property
    def media(self):
        return forms.Media(
            css={"all": ("mdeditor/css/editormd.min.css",)},
            js=("mdeditor/src/jquery.min.js", "mdeditor/editormd.min.js"),
        )


class AdminEditorMdWidget(EditorMdWidget, AdminTextareaWidget):
    def __init__(self, attrs=None):
        super(AdminEditorMdWidget, self).__init__(attrs)
