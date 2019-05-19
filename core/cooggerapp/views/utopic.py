# django
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User

# model
from core.cooggerapp.models import (Topic, UTopic, Content, Commit)


class UserTopic(TemplateView):
    "topic/@username"
    template_name = "utopic/contents-for-alt.html"

    def get_context_data(self, username, topic, **kwargs):
        user = User.objects.get(username=username)
        global_topic = Topic.objects.filter(name=topic)[0]
        contents = Content.objects.filter(user=user, 
            topic=global_topic, status="approved").order_by("created")
        utopic = UTopic.objects.filter(user=user, name=topic)[0]
        commits = Commit.objects.filter(utopic=utopic)
        context = super().get_context_data(**kwargs)
        if commits.exists():
            context["last_commit_created"] = commits[0].created        
        context["content_user"] = user
        context["queryset"] = contents
        context["utopic"] = utopic
        return context