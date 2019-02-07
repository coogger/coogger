from django import template
register = template.Library()

# core.cooggerapp
from core.cooggerapp.models import Content, Topic

@register.filter(name="topic_count")
def topic_count(topic_name, username):
    topic = Topic.objects.filter(name=topic_name)[0]
    contents = Content.objects.filter(topic=topic, status="approved")
    return contents.count()
