from cooggerapp.choices import lang_choices,category_choices

from django import template
register = template.Library()

import requests

@register.filter(name="percent")
def percent(value, arg):
    return int(value/100)

@register.filter(name="json")
def json(value, arg):
    return value[arg]

@register.filter(name="languages")
def languages(value):
    return lang_choices()

@register.filter(name="category")
def category(value):
    return category_choices()
