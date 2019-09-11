from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views import View
from django.views.generic import TemplateView, UpdateView

from ....threaded_comment.forms import ReplyForm
from ...forms import IssueForm
from ...models import Issue, UTopic
from ...views.generic.detail import CommonDetailView
from ..utils import get_current_user, paginator

# TODO if requests come same url, and query does then it should be an update


class IssueView(TemplateView):
    model = Issue
    template_name = "users/topic/detail/issues.html"

    def get_context_data(self, username, utopic_permlink, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=username)
        utopic = UTopic.objects.filter(user=user, permlink=utopic_permlink)[0]
        queryset = self.get_queryset(utopic)
        context["current_user"] = get_current_user(user)
        context["queryset"] = paginator(self.request, queryset)
        context["utopic"] = utopic
        return context

    def get_queryset(self, utopic):
        return self.model.objects.filter(utopic=utopic, status="open")


class ClosedIssueView(IssueView):
    def get_queryset(self, utopic):
        return self.model.objects.filter(utopic=utopic, status="closed")


class NewIssue(LoginRequiredMixin, View):
    template_name = "forms/create.html"
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
            form.issue_id = Issue.objects.filter(utopic=form.utopic).count() + 1
            form.save()
            return redirect(
                reverse(
                    "detail-issue",
                    kwargs=dict(
                        username=username,
                        utopic_permlink=utopic_permlink,
                        issue_id=form.issue_id,
                    ),
                )
            )


class UpdateIssue(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Issue
    fields = ["title", "body"]
    template_name = "forms/create.html"
    success_message = "Your issue updated"

    def get_object(self):
        username = self.kwargs.get("username")
        utopic_permlink = self.kwargs.get("utopic_permlink")
        issue_id = self.kwargs.get("issue_id")
        return get_object_or_404(
            self.model,
            user=self.request.user,
            utopic__user__username=username,
            utopic__permlink=utopic_permlink,
            issue_id=issue_id,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = context.get("object")
        context["current_user"] = get_current_user(object.utopic.user)
        context["utopic"] = object.utopic
        return context

    def get_success_url(self):
        return reverse(
            "detail-issue",
            kwargs=dict(
                username=self.kwargs.get("username"),
                utopic_permlink=self.kwargs.get("utopic_permlink"),
                issue_id=self.kwargs.get("issue_id"),
            ),
        )


class DetailIssue(CommonDetailView, TemplateView):
    model = Issue
    model_name = "issue"
    template_name = "users/topic/issue/detail.html"
    form_class = ReplyForm

    def get_object(self, username, utopic_permlink, issue_id):
        return get_object_or_404(
            self.model,
            utopic__user__username=username,
            utopic__permlink=utopic_permlink,
            issue_id=issue_id,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = context.get("queryset")
        context["current_user"] = get_current_user(queryset.utopic.user)
        context["utopic"] = queryset.utopic
        context["nameoflist"] = queryset.utopic
        return context


class OpenIssue(LoginRequiredMixin, View):
    def get(self, request, username, utopic_permlink, issue_id):
        utopic = get_object_or_404(
            UTopic, user__username=username, permlink=utopic_permlink
        )
        issue = Issue.objects.filter(utopic=utopic, issue_id=issue_id)
        current_username = str(request.user)
        if current_username == username or current_username == str(issue[0].user):
            issue.update(status=self.get_status)
            self.update_utopic(utopic)
            return redirect(
                reverse(
                    "detail-issue",
                    kwargs=dict(
                        username=username,
                        utopic_permlink=utopic_permlink,
                        issue_id=issue_id,
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
