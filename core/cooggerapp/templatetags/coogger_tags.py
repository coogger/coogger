# django
import random

from django import template
from django.urls import resolve
from django_bookmark.models import Bookmark

from ...threaded_comment.models import ThreadedComments
from ..choices import *
from ..models import Content, UTopic
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
    return obj.count()


@register.simple_tag
def content_count(username, value, key):
    obj = Content.objects.filter(user__username=username, status="ready")
    return model_filter({str(value): key}.items(), obj).get("queryset").count()


@register.filter
def get_count(user, name):
    if name == "utopic":
        return UTopic.objects.filter(user=user).count()
    elif name == "comments":
        return ThreadedComments.objects.filter(to=user).exclude(user=user).count()
    elif name == "bookmark":
        return Bookmark.objects.filter(user=user).count()


@register.simple_tag
def get_random(start, stop, step):
    return random.randrange(start, stop, step)
