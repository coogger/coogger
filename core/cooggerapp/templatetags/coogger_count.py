from django.contrib.auth.models import User
from django import template
register = template.Library()

# core.cooggerapp
from core.cooggerapp.models import Content, Topic

@register.filter(name="topic_count")
def topic_count(topic_name, username):
    topic = Topic.objects.filter(name=topic_name)[0]
    user = User.objects.get(username=username)
    contents = Content.objects.filter(user=user, topic=topic, status="approved")
    return contents.count()
