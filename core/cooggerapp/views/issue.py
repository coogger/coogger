# django
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse

# model
from core.cooggerapp.models import (UTopic, Issue, Commit)

# form
from core.cooggerapp.forms import IssueForm

# utils 
from core.cooggerapp.utils import paginator


class IssueView(TemplateView):
    template_name = "issue/index.html"

    def get_context_data(self, username, topic, **kwargs):
        user = authenticate(username=username)
        utopic = UTopic.objects.filter(user=user, name=topic)[0]
        issues = Issue.objects.filter(user=user, utopic=utopic, status="open")
        context = super().get_context_data(**kwargs)
        context["content_user"] = user
        context["queryset"] = issues
        context["utopic"] = utopic
        return context


class NewIssue(LoginRequiredMixin, View):
    template_name = "issue/new.html"
    form_class = IssueForm
    
    def get(self, request, username, topic):
        user = authenticate(username=username)
        context = dict(
            issue_form=self.form_class,
            content_user=user,
            utopic=UTopic.objects.filter(user=user, name=topic)[0]
        )
        return render(request, self.template_name, context)

    def post(self, request, username, topic):
        if request.user.username == username:
            user = authenticate(username=username)
            utopic = UTopic.objects.filter(user=user, name=topic)[0]
            issue_form = self.form_class(request.POST)
            if issue_form.is_valid():
                issue_form = issue_form.save(commit=False)
                issue_form.user = user
                issue_form.utopic = utopic
                issue_form.save()
                return redirect(
                    reverse(
                        "detail-issue", 
                        kwargs=dict(
                            username=request.user.username,
                            topic=topic,
                            id=issue_form.id)
                        )
                    )


class DetailIssue(TemplateView):
    template_name = "issue/detail.html"

    def get_context_data(self, username, topic, id, **kwargs):
        user = authenticate(username=username)
        issue = Issue.objects.get(id=id)
        utopic = UTopic.objects.filter(user=user, name=topic)[0]
        context = super().get_context_data(**kwargs)
        context["content_user"] = user
        context["queryset"] = issue
        context["utopic"] = utopic
        return context