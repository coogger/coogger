# django
from django.urls import resolve
from django.contrib.auth.models import User
from django import template
register = template.Library()

# core.cooggerapp
from core.cooggerapp.choices import *
from core.cooggerapp.models import Content, Topic, Commit

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
def hmanycontent(user):
    if user.is_anonymous:
        return 0
    obj = Content.objects.filter(user=user, status="approved")
    replies_count = obj.filter(reply=None).count()
    return f"{replies_count} + {obj.count() - replies_count}"

@register.filter(name="commit_count")
def commit_count(utopic):
    return Commit.objects.filter(utopic=utopic).count()
