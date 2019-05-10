# django
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate

# model
from core.cooggerapp.models import (UTopic, Issue, Commit)

# utils 
from core.cooggerapp.utils import paginator


class IssueView(TemplateView):
    template_name = "issue/index.html"

    def get_context_data(self, username, topic, **kwargs):
        user = authenticate(username=username)
        utopic = UTopic.objects.filter(name=topic)[0]
        issues = Issue.objects.filter(user=user, 
            utopic=utopic, status="open")
        utopic = UTopic.objects.filter(user=user, name=topic)[0]
        commits = Commit.objects.filter(utopic=utopic)
        context = super().get_context_data(**kwargs)
        context["content_user"] = user
        context["queryset"] = paginator(self.request, issues)
        context["utopic"] = utopic
        return context


class DetailIssue(IssueView):
    pass


class NewIssue(IssueView):
    pass