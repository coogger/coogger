from django.contrib.auth.models import User

from django import template
register = template.Library()

# cooggerapp
from cooggerapp.choices import *
from cooggerapp.models import Content

@register.filter(name="topic_count")
def topic_count(value, arg):
    user = User.objects.filter(username=arg)[0]
    queryset = Content.objects.filter(user=user, topic = value, status="approved")
    count = queryset.count()
    return count

@register.filter(name="language_count")
def language_count(value, arg):
    queryset = Content.objects.filter(language = value, status="approved")
    count = queryset.count()
    return count

@register.filter(name="categories_count")
def categories_count(value, arg):
    queryset = Content.objects.filter(category = value, status="approved")
    count = queryset.count()
    return count
