# django
from django.urls import resolve

# python
from urllib.parse import quote_plus

# cooggerapp
from cooggerapp.choices import *
from cooggerapp.models import Dapp, Content

from django import template
register = template.Library()

import requests

@register.filter(name="url_resolve")
def url_resolve(request, arg):
    return resolve(request.path_info).url_name

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
    dapp_model = Dapp.objects.filter(host_name = arg)[0]
    if dapp_model.name == "coogger":
        hmanycontent = len(Content.objects.filter(user = value,status = "approved"))
    else:
        hmanycontent = len(Content.objects.filter(dapp = dapp_model,user = value,status = "approved"))
    return hmanycontent

@register.filter(name="twitter")
def twitter(value, arg):
    return quote_plus(value)
