# django
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.utils.timezone import now
from django.db.models import F
from django.contrib import messages

# model
from core.cooggerapp.models import (UTopic, Issue)

# form
from core.cooggerapp.forms import NewIssueForm, NewIssueReplyForm

# python
import json

# TODO if requests come same url, and query does then it should be an update

class IssueView(TemplateView):
    template_name = "issue/index.html"

    def get_context_data(self, username, utopic_permlink, **kwargs):
        user = User.objects.get(username=username)
        utopic = UTopic.objects.filter(user=user, permlink=utopic_permlink)[0]
        context = super().get_context_data(**kwargs)
        context["current_user"] = user
        context["queryset"] = self.get_queryset(user, utopic)
        context["utopic"] = utopic
        return context

    def get_queryset(self, user, utopic):
        return Issue(user=user, utopic=utopic).get_open_issues


class ClosedIssueView(IssueView):

    def get_queryset(self, user, utopic):
        return Issue(user=user, utopic=utopic).get_closed_issues


class NewIssue(LoginRequiredMixin, View):
    template_name = "issue/new.html"
    form_class = NewIssueForm
    
    def get(self, request, username, utopic_permlink):
        user = User.objects.get(username=username)
        context = dict(
            issue_new_form=self.form_class,
            current_user=user,
            utopic=UTopic.objects.filter(user=user, permlink=utopic_permlink)[0]
        )
        return render(request, self.template_name, context)

    def post(self, request, username, utopic_permlink):
        user = User.objects.get(username=username)
        utopic = UTopic.objects.filter(user=user, permlink=utopic_permlink)[0]
        issue_new_form = self.form_class(request.POST)
        if issue_new_form.is_valid():
            issue_new_form = issue_new_form.save(commit=False)
            if not issue_new_form.title:
                messages.error(request, "You can not pass the title field")
                return self.get(request, username, utopic_permlink)
            issue_new_form.user = request.user
            issue_new_form.utopic = utopic
            issue_new_form.issue_save()
            return redirect(
                reverse(
                    "detail-issue", 
                    kwargs=dict(
                        username=username,
                        utopic_permlink=utopic_permlink,
                        permlink=issue_new_form.permlink)
                    )
                )


class DetailIssue(View):
    template_name = "issue/detail.html"
    form_class = NewIssueReplyForm

    def get(self, request, username, utopic_permlink, permlink):
        user = User.objects.get(username=username)
        utopic = UTopic.objects.get(user=user, permlink=utopic_permlink)
        issue = Issue.objects.get(utopic=utopic, permlink=permlink)
        context = dict(
            reply_form=self.form_class,
            current_user=user,
            queryset=issue,
            utopic=utopic,
            md_editor=True,
        )
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, username, utopic_permlink, permlink):
        if request.is_ajax:
            user = User.objects.get(username=username)
            utopic = UTopic.objects.filter(user=user, permlink=utopic_permlink)[0]
            issue = Issue.objects.get(user=user, utopic=utopic, permlink=permlink)
            reply_form = self.form_class(request.POST)
            if reply_form.is_valid():
                reply_form = reply_form.save(commit=False)
                reply_form.user = user
                reply_form.utopic = utopic
                reply_form.reply = issue
                reply_form.issue_save()
                return HttpResponse(
                    json.dumps(
                        dict(
                            username=str(reply_form.user),
                            utopic_permlink=reply_form.utopic.permlink,
                            parent_permlink=reply_form.parent_permlink,
                            parent_username=reply_form.parent_username,
                            created=str(reply_form.created),
                            reply_count=reply_form.reply_count,
                            status=reply_form.status,
                            reply=reply_form.reply_id,
                            body=reply_form.body,
                            title=reply_form.title,
                            permlink=reply_form.permlink,
                            avatar_url=reply_form.user.githubauthuser.avatar_url,
                            )
                        )
                    )


class OpenIssue(View):

    @method_decorator(login_required)
    def get(self, request, username, utopic_permlink, permlink):
        user = User.objects.get(username=username)
        utopic_obj = UTopic.objects.filter(user=user, permlink=utopic_permlink)
        issue = Issue.objects.filter(
            utopic=utopic_obj[0], 
            permlink=permlink
        )
        if request.user == user or request.user == issue[0].user:
            issue.update(
                status=self.get_status,
                last_update=now())
            self.update_utopic(utopic_obj)
            return redirect(
                reverse(
                    "detail-issue", 
                    kwargs=dict(
                        username=username,
                        utopic_permlink=utopic_permlink,
                        permlink=permlink)
                    )
                )
    
    def update_utopic(self, utopic_obj):
        utopic_obj.update(
            open_issue=(F("open_issue") + 1),
            closed_issue=(F("closed_issue") - 1),
        )

    @property
    def get_status(self):
        return "open"


class ClosedIssue(OpenIssue):

    def update_utopic(self, utopic_obj):
        utopic_obj.update(
            open_issue=(F("open_issue") - 1),
            closed_issue=(F("closed_issue") + 1),
        )

    @property
    def get_status(self):
        return "closed"