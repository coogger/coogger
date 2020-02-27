from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from apps.md_editor.configs import default_config

register = template.Library()


@register.filter
def markdown_to_html(value, arg):
    context = dict(markdown=value, id=arg, config=default_config)
    return mark_safe(render_to_string("show.html", context))
