from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

from ...threaded_comment.forms import ReplyForm
from ..models import Commit, UTopic
from ..views.generic.detail import CommonDetailView
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


class CommitDetail(CommonDetailView, TemplateView):
    template_name = "users/detail-topic/commit.html"
    model = Commit
    model_name = "commit"
    form_class = ReplyForm

    def get_object(self, username, topic_permlink, hash):
        return Commit.objects.get(hash=hash)

    def get_context_data(self, username, topic_permlink, hash, **kwargs):
        context = super().get_context_data(
            **dict(username=username, topic_permlink=topic_permlink, hash=hash)
        )
        queryset = context.get("queryset")
        context["current_user"] = get_object_or_404(User, username=username)
        context["nameoflist"] = queryset.utopic
        context["commit"] = queryset
        return context
