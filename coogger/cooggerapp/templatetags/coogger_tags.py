# python
from urllib.parse import quote_plus

# cooggerapp
from cooggerapp.choices import *
from cooggerapp.models import Community,Content

from django import template
register = template.Library()

import requests

@register.filter(name="percent")
def percent(value, arg):
    return int(value/100)

@register.filter(name="split")
def split(value, arg):
    return value.split(arg)

@register.filter(name="json")
def json(value, arg):
    return value[arg]

@register.filter(name="hmanycontent")
def hmanycontent(value, arg):
    community_model = Community.objects.filter(host_name = arg)[0]
    if community_model.name == "coogger":
        hmanycontent = len(Content.objects.filter(user = value,status = "approved"))
    else:
        hmanycontent = len(Content.objects.filter(community = community_model,user = value,status = "approved"))
    return hmanycontent

@register.filter(name="twitter")
def twitter(value, arg):
    return quote_plus(value)
