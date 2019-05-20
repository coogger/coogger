# django
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User

# model
from core.cooggerapp.models import (UTopic, Commit)

# utils 
from core.cooggerapp.views.utils import paginator


class Commits(TemplateView):
    template_name = "utopic/commits.html"

    def get_context_data(self, username, topic, **kwargs):
        user = User.objects.get(username=username)
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
        context["content_user"] = User.objects.get(username=username)
        context["commit"] = Commit.objects.filter(hash=hash)[0]
        return context