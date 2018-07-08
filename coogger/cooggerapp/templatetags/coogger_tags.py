from cooggerapp.choices import *
from cooggerapp.models import Community,Content

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
    return eval("coogger_community_left()")

@register.filter(name="category")
def category(value):
    return eval("coogger_community_right()")

@register.filter(name="hmanycontent")
def hmanycontent(value, arg):
    community_model = Community.objects.filter(host_name = arg)[0]
    hmanycontent = len(Content.objects.filter(community = community_model,user = value))
    return hmanycontent
