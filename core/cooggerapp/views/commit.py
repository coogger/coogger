from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

from ..models import Commit, UTopic
from .utils import paginator


class Commits(TemplateView):
    template_name = "users/detail-topic/commits.html"

    def get_context_data(self, username, topic_permlink, **kwargs):
        user = get_object_or_404(User, username=username)
        utopic = UTopic.objects.get(user__username=username, permlink=topic_permlink)
        queryset = Commit.objects.filter(utopic=utopic)
        if user != self.request.user:
            queryset = queryset.filter(content__status="ready")
        context = super().get_context_data(**kwargs)
        context["current_user"] = user
        context["queryset"] = paginator(self.request, queryset)
        context["utopic"] = utopic
        if queryset.exists():
            context["last_update"] = queryset[0].created
        return context


class CommitDetail(TemplateView):
    template_name = "users/detail-topic/commit.html"
    # TODO
    # url '@username/topic_permlink/commit/hash/'
    # or url can be
    ##url '/commit/hash/' because hash is unique

    def get_context_data(self, username, topic_permlink, hash, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_user"] = get_object_or_404(User, username=username)
        context["commit"] = Commit.objects.filter(hash=hash)[0]
        return context
