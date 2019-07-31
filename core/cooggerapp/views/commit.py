#django
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User

#model
from ..models import (UTopic, Commit)

#utils
from .utils import paginator


class Commits(TemplateView):
    template_name = "users/detail-topic/commits.html"

    def get_context_data(self, username, topic_permlink, **kwargs):
        user = User.objects.get(username=username)
        utopic = UTopic.objects.get(user__username=username, permlink=topic_permlink)
        commits = Commit.objects.filter(utopic=utopic)
        context = super().get_context_data(**kwargs)
        context["current_user"] = user
        context["queryset"] = paginator(self.request, commits)
        context["utopic"] = utopic
        if commits.exists():
            context["last_update"] = commits[0].created
        return context


class CommitDetail(TemplateView):
    template_name = "users/detail-topic/commit.html"
    #TODO
    #url '@username/topic_permlink/commit/hash/'
    #or url can be
    ##url '/commit/hash/' because hash is unique

    def get_context_data(self, username, topic_permlink, hash, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_user"] = User.objects.get(username=username)
        context["commit"] = Commit.objects.filter(hash=hash)[0]
        return context