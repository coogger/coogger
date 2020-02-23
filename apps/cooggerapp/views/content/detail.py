from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ....threaded_comment.forms import ReplyForm
from ...models import Commit, Content
from ..generic.detail import CommonDetailView
from ..utils import get_current_user


class Detail(CommonDetailView, TemplateView):
    model = Content
    model_name = "content"
    template_name = "content/detail/detail.html"
    form_class = ReplyForm

    def get_object(self, username, permlink):
        if username == self.request.user.username:
            return get_object_or_404(Content, user__username=username, permlink=permlink)
        return get_object_or_404(Content, user__username=username, permlink=permlink, utopic__status="public")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = context.get("queryset")
        context["current_user"] = get_current_user(queryset.user)
        context["current_page_permlink"] = queryset.permlink
        context["nameoflist"] = queryset.utopic
        return context


class TreeDetail(TemplateView):
    template_name = "content/detail/tree.html"
    # TODO show all replies acording to commit date,
    # use Detail class but all data must be acording to commit date

    def get_context_data(self, username, topic_permlink, hash, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=username)
        context["current_user"] = get_current_user(user)
        if username == self.request.user.username:
            context["queryset"] = Commit.objects.get(hash=hash)
        else:
            context["queryset"] = Commit.objects.get(hash=hash, utopic__status="public")
        return context
