from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, UpdateView

from ....threaded_comment.forms import ReplyForm
from ...models import Commit, UTopic
from ...views.generic.detail import CommonDetailView
from ..utils import paginator


class Commits(TemplateView):
    template_name = "users/topic/detail/commits.html"
    commits = Commit.objects.approved_commits

    def get_context_data(self, username, topic_permlink, **kwargs):
        user = get_object_or_404(User, username=username)
        utopic = UTopic.objects.get(user__username=username, permlink=topic_permlink)
        filter_by_username = self.request.GET.get("username", None)
        if filter_by_username:
            queryset = self.commits.filter(
                user__username=filter_by_username, utopic=utopic
            )
        else:
            queryset = self.commits.filter(utopic=utopic)
        context = super().get_context_data(**kwargs)
        context["current_user"] = user
        context["queryset"] = paginator(self.request, queryset)
        context["utopic"] = utopic
        return context


class CommitDetail(CommonDetailView, TemplateView):
    template_name = "users/topic/commit/commit.html"
    model = Commit
    model_name = "commit"
    form_class = ReplyForm

    def get_object(self, username, topic_permlink, hash):
        obj = Commit.objects.get(hash=hash)
        if obj.status != "approved":
            # NOTE when commit it is a contribute
            self.template_name = "users/topic/commit/contribution.html"
        return obj

    def get_context_data(self, username, topic_permlink, hash, **kwargs):
        context = super().get_context_data(
            **dict(username=username, topic_permlink=topic_permlink, hash=hash)
        )
        queryset = context.get("queryset")
        context["current_user"] = get_object_or_404(User, username=username)
        context["nameoflist"] = queryset.utopic
        context["commit"] = queryset
        return context


class CommitUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Commit
    fields = ["body", "msg"]
    template_name = "forms/create.html"
    success_message = "Your commit updated"

    def get_object(self):
        hash = self.kwargs.get("hash")
        obj = get_object_or_404(self.model, hash=hash)
        if obj.user == self.request.user:
            if obj.status == "approved":
                raise Http404("Your commit's approved, thus we can not update.")
        else:
            raise Http404("Permission denied.")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = context.get("object")
        context["current_user"] = object.utopic.user
        context["utopic"] = object.utopic
        return context

    def get_success_url(self):
        commit = Commit.objects.get(hash=self.kwargs.get("hash"))
        return reverse(
            "commit",
            kwargs=dict(
                username=commit.user,
                topic_permlink=commit.utopic.permlink,
                hash=commit.hash,
            ),
        )
