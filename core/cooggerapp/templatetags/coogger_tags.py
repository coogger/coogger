# django
import random

import requests
from django import template
from django.contrib.auth.models import User
from django.urls import resolve

from ..choices import *
from ..models import Commit, Content, Topic
from ..views.utils import model_filter

register = template.Library()


@register.filter
def url_resolve(request, arg):
    return resolve(request.path_info).url_name


@register.filter
def percent(value, arg):
    return int(value / 100)


@register.filter
def split(value, arg):
    return value.split(arg)


@register.filter
def json(value, arg):
    return value[arg]


@register.filter
def hmanycontent(user):
    if user.is_anonymous:
        return 0
    obj = Content.objects.filter(user=user, status="ready")
    replies_count = obj.filter(reply=None).count()
    return f"{replies_count} + {obj.count() - replies_count}"


@register.simple_tag
def content_count(username, value, key):
    obj = Content.objects.filter(user__username=username, status="ready", reply=None)
    return model_filter({str(value): key}.items(), obj).get("queryset").count()


@register.simple_tag
def get_random(start, stop, step):
    return random.randrange(start, stop, step)


@register.filter
def commit_count(utopic):
    return Commit.objects.filter(utopic=utopic).count()
