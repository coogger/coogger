# django
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate

# model
from core.cooggerapp.models import (Topic, UTopic, Content, Commit)

# utils 
from core.cooggerapp.utils import paginator

class UserTopic(TemplateView):
    "topic/@username"
    template_name = "utopic/contents-for-alt.html"

    def get_context_data(self, username, topic, **kwargs):
        user = authenticate(username=username)
        global_topic = Topic.objects.filter(name=topic)[0]
        contents = Content.objects.filter(user=user, 
            topic=global_topic, status="approved").order_by("created")
        utopic = UTopic.objects.filter(user=user, name=topic)[0]
        commits = Commit.objects.filter(utopic=utopic)
        context = super().get_context_data(**kwargs)
        context["content_user"] = user
        context["queryset"] = paginator(self.request, contents)
        context["last_commit_created"] = commits[0].created
        context["utopic"] = utopic
        return context

class Commits(TemplateView):
    template_name = "utopic/commits.html"

    def get_context_data(self, username, topic, **kwargs):
        user = authenticate(username=username)
        utopic = UTopic.objects.filter(user=user, name=topic)[0]
        commits = Commit.objects.filter(utopic=utopic)
        context = super().get_context_data(**kwargs)
        context["content_user"] = user
        context["queryset"] = paginator(self.request, commits)
        context["utopic"] = utopic
        return context
        
class CommitDetail(TemplateView):
    template_name = "utopic/commit.html"

    def get_context_data(self, username, topic, hash, **kwargs):
        context = super().get_context_data(**kwargs)
        context["content_user"] = authenticate(username=username)
        context["commit"] = Commit.objects.filter(hash=hash)[0]
        return context


class Issue(TemplateView):
    pass