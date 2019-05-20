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
from core.cooggerapp.forms import NewIssueForm, ReplyIssueForm

# python
import json


class IssueView(TemplateView):
    template_name = "issue/index.html"

    def get_context_data(self, username, topic, **kwargs):
        user = User.objects.get(username=username)
        utopic = UTopic.objects.filter(user=user, name=topic)[0]
        context = super().get_context_data(**kwargs)
        context["content_user"] = user
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
    
    def get(self, request, username, topic):
        user = User.objects.get(username=username)
        context = dict(
            issue_form=self.form_class,
            content_user=user,
            utopic=UTopic.objects.filter(user=user, name=topic)[0]
        )
        return render(request, self.template_name, context)

    def post(self, request, username, topic):
        user = User.objects.get(username=username)
        utopic = UTopic.objects.filter(user=user, name=topic)[0]
        issue_form = self.form_class(request.POST)
        if issue_form.is_valid():
            issue_form = issue_form.save(commit=False)
            if not issue_form.title:
                messages.error(request, "You can not pass the title field")
                return self.get(request, username, topic)
            issue_form.user = request.user
            issue_form.utopic = utopic
            issue_form.issue_save()
            return redirect(
                reverse(
                    "detail-issue", 
                    kwargs=dict(
                        username=username,
                        topic=topic,
                        permlink=issue_form.permlink)
                    )
                )


class DetailIssue(View):
    template_name = "issue/detail.html"
    form_class = ReplyIssueForm

    def get(self, request, username, topic, permlink):
        user = User.objects.get(username=username)
        utopic = UTopic.objects.get(user=user, name=topic)
        issue = Issue.objects.get(utopic=utopic, permlink=permlink)
        context = dict(
            content_user=user,
            queryset=issue,
            utopic=utopic,
            md_editor=True,
        )
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, username, topic, permlink):
        if request.is_ajax:
            user = User.objects.get(username=username)
            utopic = UTopic.objects.filter(user=user, name=topic)[0]
            issue = Issue.objects.get(user=user, utopic=utopic, permlink=permlink)
            issue_form = self.form_class(request.POST)
            if issue_form.is_valid():
                issue_form = issue_form.save(commit=False)
                issue_form.user = user
                issue_form.utopic = utopic
                issue_form.reply = issue
                issue_form.issue_save()
                new_reply = Issue.objects.get(
                    user=user, 
                    utopic=utopic, 
                    permlink=issue_form.permlink)
                return HttpResponse(
                    json.dumps(
                        dict(
                            username=new_reply.username,
                            topic_name=new_reply.topic_name,
                            parent_permlink=new_reply.parent_permlink,
                            parent_username=new_reply.parent_username,
                            created=str(new_reply.created),
                            reply_count=new_reply.reply_count,
                            status=new_reply.status,
                            reply=new_reply.reply_id,
                            body=new_reply.body,
                            title=new_reply.title,
                            permlink=new_reply.permlink,
                            )
                        )
                    )


class OpenIssue(View):

    @method_decorator(login_required)
    def get(self, request, username, topic, permlink):
        user = User.objects.get(username=username)
        utopic_obj = UTopic.objects.filter(user=user, name=topic)
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
                        topic=topic,
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