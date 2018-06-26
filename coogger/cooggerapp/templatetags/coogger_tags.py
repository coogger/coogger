from cooggerapp.choices import lang_choices,type_choices

from django import template
from django.conf import settings
STEEM = settings.STEEM
register = template.Library()

# steem
from easysteem.easysteem import Oogg

import requests

@register.filter(name="upvote")
def upvote(value, arg):# kullanıcı upvote atmış mı atmamışmı
    try:
        voters = Oogg(node = STEEM).voters(value.user.username,value.permlink)
    except:
        return None
    if arg in voters:
        return True
    return False

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
    return type_choices()
