from django.contrib.auth.models import User

from django import template
register = template.Library()

# cooggerapp
from cooggerapp.choices import *
from cooggerapp.models import Content

@register.filter(name="topic_count")
def topic_count(value, arg):
    contents = Content.objects.filter(topic = value, status="approved")
    if arg != "":
        user = User.objects.filter(username=arg)[0]
        queryset = contents.filter(user=user)
    else:
        queryset = contents
    return queryset.count()

@register.filter(name="language_count")
def language_count(value, arg):
    if arg.name == "coogger":
        queryset = Content.objects.filter(language = value, status="approved")
    else:
        queryset = Content.objects.filter(language = value, status="approved", dapp=arg)
    count = queryset.count()
    return count

@register.filter(name="categories_count")
def categories_count(value, arg):
    if arg.name == "coogger":
        queryset = Content.objects.filter(category = value, status="approved")
    else:
        queryset = Content.objects.filter(category = value, status="approved", dapp=arg)
    count = queryset.count()
    return count
