from cooggerapp.choices import *
from cooggerapp.models import Community,Content
from cooggerapp.choices import make_choices

from django import template
register = template.Library()

import requests

@register.filter(name="percent")
def percent(value, arg):
    return int(value/100)

@register.filter(name="json")
def json(value, arg):
    return value[arg]

@register.filter(name="categories")
def categories(value, arg):
    community_model = Community.objects.filter(host_name = arg)[0]
    return make_choices(eval(str(community_model.name)+"_categories()"))

@register.filter(name="languages")
def languages(value, arg):
    community_model = Community.objects.filter(host_name = arg)[0]
    return make_choices(eval(str(community_model.name)+"_languages()"))

@register.filter(name="hmanycontent")
def hmanycontent(value, arg):
    community_model = Community.objects.filter(host_name = arg)[0]
    hmanycontent = len(Content.objects.filter(community = community_model,user = value,status = "approved"))
    return hmanycontent
