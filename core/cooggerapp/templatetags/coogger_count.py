from django.contrib.auth.models import User

from django import template
register = template.Library()

# core.cooggerapp
from core.cooggerapp.choices import *
from core.cooggerapp.models import Content, Topic

@register.filter(name="topic_count")
def topic_count(topic_name, username):
    try:
        topic = Topic.objects.filter(name=topic_name)[0]
    except IndexError:
        Topic(name=topic_name).save()
        topic = Topic.objects.filter(name=topic_name)[0]
    contents = Content.objects.filter(topic = topic, status="approved")
    if username != "":
        user = User.objects.filter(username=username)[0]
        queryset = contents.filter(user=user)
    else:
        queryset = contents
    return queryset.count()
