from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils.timezone import now
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView

from ..forms import IssueForm, IssueReplyForm
from ..models import Issue, UTopic
from ..views.generic.detail import DetailPostView
from .utils import paginator

# TODO if requests come same url, and query does then it should be an update


class IssueView(TemplateView):
    model = Issue
    template_name = "issue/index.html"

    def get_context_data(self, username, utopic_permlink, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=username)
        utopic = UTopic.objects.filter(user=user, permlink=utopic_permlink)[0]
        queryset = self.get_queryset(utopic)
        context["current_user"] = user
        context["queryset"] = paginator(self.request, queryset)
        context["utopic"] = utopic
        if queryset.exists():
            context["last_update"] = queryset[0].created
        return context

    def get_queryset(self, utopic):
        return self.model.objects.filter(utopic=utopic, status="open", reply=None)


class ClosedIssueView(IssueView):
    def get_queryset(self, utopic):
        return self.model.objects.filter(utopic=utopic, status="closed", reply=None)


class NewIssue(LoginRequiredMixin, View):
    template_name = "issue/new.html"
    form_class = IssueForm

    def get(self, request, username, utopic_permlink):
        user = get_object_or_404(User, username=username)
        context = dict(
            form=self.form_class,
            current_user=user,
            utopic=UTopic.objects.filter(user=user, permlink=utopic_permlink)[0],
        )
        return render(request, self.template_name, context)

    def post(self, request, username, utopic_permlink):
        user = get_object_or_404(User, username=username)
        utopic = UTopic.objects.filter(user=user, permlink=utopic_permlink)[0]
        form = self.form_class(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            if not form.title:
                messages.error(request, "You can not pass the title field")
                return self.get(request, username, utopic_permlink)
            form.user = request.user
            form.utopic = utopic
            form.issue_id = (
                Issue.objects.filter(utopic=form.utopic, reply=None).count() + 1
            )
            form.save()
            return redirect(
                reverse(
                    "detail-issue",
                    kwargs=dict(
                        username=username,
                        utopic_permlink=utopic_permlink,
                        permlink=form.permlink,
                    ),
                )
            )


class UpdateIssue(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Issue
    fields = ["title", "body"]
    template_name = "issue/new.html"
    success_message = "Your issue updated"

    def get_object(self):
        username = self.kwargs.get("username")
        utopic_permlink = self.kwargs.get("utopic_permlink")
        permlink = self.kwargs.get("permlink")
        return get_object_or_404(
            self.model,
            user=self.request.user,
            utopic__user__username=username,
            utopic__permlink=utopic_permlink,
            permlink=permlink,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = context.get("object")
        context["current_user"] = object.utopic.user
        context["utopic"] = object.utopic
        return context

    def get_success_url(self):
        return reverse(
            "detail-issue",
            kwargs=dict(
                username=self.kwargs.get("username"),
                utopic_permlink=self.kwargs.get("utopic_permlink"),
                permlink=self.kwargs.get("permlink"),
            ),
        )


class DetailIssue(DetailPostView, View):
    model = Issue
    model_name = "issue"
    template_name = "issue/detail.html"
    form_class = IssueReplyForm
    # fields that remain the same when commented.
    same_fields = ["title", "utopic"]
    # json respon fields after commented
    response_field = [
        "id",
        "user.username",
        "utopic.permlink",
        "parent_permlink",
        "parent_user",
        "created",
        "reply_count",
        "status",
        "reply_id",
        "body",
        "title",
        "permlink",
        "user.githubauthuser.avatar_url",
        "get_absolute_url",
    ]
    update_field = dict(status=None)

    def get_object(self, username, utopic_permlink, permlink):
        return get_object_or_404(
            self.model,
            utopic__user__username=username,
            utopic__permlink=utopic_permlink,
            permlink=permlink,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = context.get("queryset")
        context["current_user"] = queryset.utopic.user
        context["utopic"] = queryset.utopic
        context["last_update"] = queryset.last_update
        context["nameoflist"] = queryset.utopic
        return context


class OpenIssue(LoginRequiredMixin, View):
    def get(self, request, username, utopic_permlink, permlink):
        utopic = get_object_or_404(
            UTopic, user__username=username, permlink=utopic_permlink
        )
        issue = Issue.objects.filter(utopic=utopic, permlink=permlink)
        current_username = str(request.user)
        if current_username == username or current_username == str(issue[0].user):
            issue.update(status=self.get_status, last_update=now())
            self.update_utopic(utopic)
            return redirect(
                reverse(
                    "detail-issue",
                    kwargs=dict(
                        username=username,
                        utopic_permlink=utopic_permlink,
                        permlink=permlink,
                    ),
                )
            )

    def update_utopic(self, utopic):
        utopic.open_issue += 1
        utopic.closed_issue -= 1
        utopic.save()

    @property
    def get_status(self):
        return "open"


class ClosedIssue(OpenIssue):
    def update_utopic(self, utopic):
        utopic.open_issue -= 1
        utopic.closed_issue += 1
        utopic.save()

    @property
    def get_status(self):
        return "closed"
