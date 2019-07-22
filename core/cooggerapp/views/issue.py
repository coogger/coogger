# django
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.utils.timezone import now
from django.db.models import F
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db.utils import IntegrityError
from django.views.generic.edit import UpdateView

# model
from ..models import (UTopic, Issue)
from django_page_views.models import DjangoViews

# form
from ..forms import IssueForm, IssueReplyForm

# python
import json

# utils
from .utils import paginator

# TODO if requests come same url, and query does then it should be an update

class IssueView(TemplateView):
    model = Issue
    template_name = "issue/index.html"

    def get_context_data(self, username, utopic_permlink, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=username)
        utopic = UTopic.objects.filter(user=user, permlink=utopic_permlink)[0]
        queryset = self.get_queryset(utopic)
        context["current_user"] = user
        context["queryset"] = paginator(self.request, queryset)
        context["utopic"] = utopic
        if queryset.exists():
            context["last_update"] = queryset[0].created
        return context

    def get_queryset(self, utopic):
        return self.model.objects.filter(
            utopic=utopic,
            status="open", 
            reply=None
        )


class ClosedIssueView(IssueView):

    def get_queryset(self, utopic):
        return self.model.objects.filter(
            utopic=utopic,
            status="closed", 
            reply=None
        )


class NewIssue(LoginRequiredMixin, View):
    template_name = "issue/new.html"
    form_class = IssueForm
    
    def get(self, request, username, utopic_permlink):
        user = User.objects.get(username=username)
        context = dict(
            form=self.form_class,
            current_user=user,
            utopic=UTopic.objects.filter(user=user, permlink=utopic_permlink)[0]
        )
        return render(request, self.template_name, context)

    def post(self, request, username, utopic_permlink):
        user = User.objects.get(username=username)
        utopic = UTopic.objects.filter(user=user, permlink=utopic_permlink)[0]
        form = self.form_class(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            if not form.title:
                messages.error(request, "You can not pass the title field")
                return self.get(request, username, utopic_permlink)
            form.user = request.user
            form.utopic = utopic
            form.issue_id = Issue.objects.filter(
                utopic=form.utopic,
                reply=None
            ).count() + 1
            form.save()
            if request.user != user:
                self.form_class.send_mail(form)
            return redirect(
                reverse(
                    "detail-issue", 
                    kwargs=dict(
                        username=username,
                        utopic_permlink=utopic_permlink,
                        permlink=form.permlink)
                    )
                )


class UpdateIssue(LoginRequiredMixin, UpdateView):
    model = Issue
    fields = ["title", "body"]
    template_name = "issue/new.html"

    def get_object(self):
        username = self.kwargs.get("username")
        utopic_permlink = self.kwargs.get("utopic_permlink")
        permlink = self.kwargs.get("permlink")
        return get_object_or_404(
            self.model, 
            user=self.request.user, 
            utopic__user__username=username,
            utopic__permlink=utopic_permlink,
            permlink=permlink
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = context.get("object")
        context["current_user"] = object.utopic.user
        context["utopic"] = object.utopic
        return context

    def get_success_url(self):
        return reverse("detail-issue", kwargs=dict(
                username=self.kwargs.get("username"),
                utopic_permlink=self.kwargs.get("utopic_permlink"),
                permlink=self.kwargs.get("permlink"),
            )
        )


class DetailIssue(View):
    model = Issue
    template_name = "issue/detail.html"
    reply_form_class = IssueReplyForm
    #fields that remain the same when commented.
    same_fields = [
        "title",
        "utopic",
    ]
    #json respon fields after commented
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

    def save_view(self, request, id):
        get_view, created = DjangoViews.objects.get_or_create(
            content_type=ContentType.objects.get(
                app_label="cooggerapp", 
                model="issue"
            ), 
            object_id=id
        )
        try:
            get_view.ips.add(request.ip_model)
        except IntegrityError:
            pass

    def get_object(self, username, utopic_permlink, permlink):
        return get_object_or_404(
            self.model, 
            utopic__user__username=username,
            utopic__permlink=utopic_permlink,
            permlink=permlink
        )

    def get(self, request, username, utopic_permlink, permlink):
        issue = self.get_object(username, utopic_permlink, permlink)
        self.save_view(request, issue.id)
        context = dict(
            reply_form=self.reply_form_class,
            current_user=issue.user,
            queryset=issue,
            utopic=issue.utopic,
            last_update=issue.last_update
        )
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, username, utopic_permlink, permlink):
        reply_form = self.reply_form_class(request.POST)
        if reply_form.is_valid():
            issue = self.get_object(username, utopic_permlink, permlink)
            reply_form = reply_form.save(commit=False)
            reply_form.user = request.user
            for field in self.same_fields:
                setattr(reply_form, field, getattr(issue, field))
            reply_form.reply = issue
            reply_form.status = None
            reply_form.save()
            context = dict()
            for field in self.response_field:
                s = field.split(".")
                if len(s) == 1:
                    context[field] = str(getattr(reply_form, field))
                else:
                    obj = reply_form
                    for f in s:
                        obj = getattr(obj, f)
                    value = str(obj)
                    context[s[-1]] = value
            return HttpResponse(json.dumps(context))


class OpenIssue(LoginRequiredMixin, View):

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