from django.contrib.auth.models import User

from django import template
register = template.Library()

# core.cooggerapp
from core.cooggerapp.choices import *
from core.cooggerapp.models import Content

@register.filter(name="topic_count")
def topic_count(value, arg):
    contents = Content.objects.filter(topic = value, status="approved")
    if arg != "":
        user = User.objects.filter(username=arg)[0]
        queryset = contents.filter(user=user)
    else:
        queryset = contents
    return queryset.count()
