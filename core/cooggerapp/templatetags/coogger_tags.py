# django
from django.urls import resolve
from django.contrib.auth.models import User
from django import template
register = template.Library()

# python
from urllib.parse import quote_plus

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
    return Content.objects.filter(user=user, status="approved").count()

@register.filter(name="twitter")
def twitter(value, arg):
    return quote_plus(value)

@register.filter(name="topic_count")
def topic_count(utopic):
    topic_name, user = utopic.name, utopic.user
    topic = Topic.objects.filter(name=topic_name)[0]
    contents = Content.objects.filter(user=user, topic=topic, status="approved")
    return contents.count()

@register.filter(name="commit_count")
def commit_count(utopic):
    return Commit.objects.filter(utopic=utopic).count()
