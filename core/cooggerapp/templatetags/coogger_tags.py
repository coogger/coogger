# django
import random

from django import template
from django.urls import resolve

from ..choices import *
from ..models import Commit, Content
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

@register.filter
def calculate_percent_utopic(utopic, choice):
    contents = Content.objects.filter(utopic=utopic, reply=None)
    how_many_content = utopic.how_many
    corl = dict()
    for content in contents:
        try:
            corl[getattr(content, choice)] += 1
        except KeyError:
            corl[getattr(content, choice)] = 1
    context = list()
    for model, count in corl.items():
        context.append(
            dict(
                model=model,
                count=count, 
                percent=f"{round((100 * count) / how_many_content, 2)}%"
            )
        )
    return context
