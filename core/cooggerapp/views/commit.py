# django
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User

# model
from core.cooggerapp.models import (UTopic, Commit)

# utils 
from core.cooggerapp.views.utils import paginator


class Commits(TemplateView):
    template_name = "utopic/commits.html"

    def get_context_data(self, username, topic_permlink, **kwargs):
        user = User.objects.get(username=username)
        utopic = UTopic.objects.filter(user=user, permlink=topic_permlink)[0]
        commits = Commit.objects.filter(utopic=utopic)
        context = super().get_context_data(**kwargs)
        context["content_user"] = user
        context["queryset"] = paginator(self.request, commits)
        context["utopic"] = utopic
        return context


class CommitDetail(TemplateView):
    template_name = "utopic/commit.html"
    # TODO
    # url '@username/topic_permlink/commit/hash/'
    # or url can be
    # # url '/commit/hash/' because hash is unique

    def get_context_data(self, username, topic_permlink, hash, **kwargs):
        context = super().get_context_data(**kwargs)
        context["content_user"] = User.objects.get(username=username)
        context["commit"] = Commit.objects.filter(hash=hash)[0]
        return context