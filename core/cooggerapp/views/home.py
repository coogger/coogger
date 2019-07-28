# django
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.urls import resolve
from django.conf import settings
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

# form
from ..forms import ReportsForm

# models
from ..models import Content, SearchedWords, ReportModel, Topic, Issue

# utils
from .utils import paginator


class Home(TemplateView):
    template_name = "card/blogs.html"
    introduction_template_name = "home/introduction.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.url_name = resolve(self.request.path_info).url_name
        self.is_authenticated = self.request.user.is_authenticated
        if not self.is_authenticated and self.url_name == "home":
            context["introduction"] = True
            self.template_name = self.introduction_template_name
        context["sort_topics"] = self.sort_topics() # just pc
        context["issues"] = Issue.objects.filter(
            reply=None, status="open"
        )[: settings.PAGE_SIZE]
        context["queryset"] = paginator(self.request, self.get_queryset())
        context["insection_left"] = True
        context["insection_right"] = True
        return context

    def get_queryset(self):
        queryset = Content.objects.filter(status="approved", reply=None)
        if not self.is_authenticated and self.url_name == "home":
            return self.get_queryset_to_introduction(queryset)
        return queryset

    @staticmethod
    def get_queryset_to_introduction(queryset):
        check, posts = [], []
        for query in queryset:
            if query.user not in check:
                check.append(query.user)
                posts.append(query)
            if len(posts) == settings.PAGE_SIZE:
                break
        return posts

    @staticmethod
    def sort_topics():
        topics = list()
        for topic in Topic.objects.all():
            if (topic not in topics) and (len(topics) <= 30) and (not topic.editable):
                topics.append(topic)
        return topics


class Report(LoginRequiredMixin, View):
    form_class = ReportsForm
    template_name = "home/report.html"

    def get(self, request, content_id, *args, **kwargs):
        if request.is_ajax():
            report_form = self.form_class()
            context = dict(
                report_form=report_form,
                content_id=content_id,
            )
            return render(request, self.template_name, context)
        raise Http404

    def post(self, request, content_id, *args, **kwargs):
        report_form = self.form_class(request.POST)
        if report_form.is_valid():
            content = Content.objects.get(id=content_id)
            if ReportModel.objects.filter(user=request.user, content=content).exists():
                messages.error(request, "Your complaint is in the evaluation process.")
                return redirect(reverse("home"))
            report_form = report_form.save(commit=False)
            report_form.user = request.user
            report_form.content = content
            report_form.save()
            messages.error(request, "Your complaint has been received.")
            return redirect(reverse("home"))
        return HttpResponse(self.get(request, *args, **kwargs))


class Search(Home):
    template_name = "card/blogs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["queryset"] = paginator(self.request, self.get_queryset())
        return context

    def get_queryset(self):
        name = self.request.GET["query"].lower()
        SearchedWords(word=name).save()
        q = Q(title__contains=name) | Q(body__contains=name)
        queryset = Content.objects.filter(q).filter(status="approved", reply=None)
        return queryset


class Feed(Home):
    # TODO this class must be improved
    # make a new model for this op
    template_name = "card/blogs.html"

    def get_context_data(self, username, **kwargs):
        self.username = username
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        following = list(User.objects.get(username=self.username).follow.following.all())
        queryset = list()
        contents = Content.objects.filter(status="approved")
        for user in following:
            queryset += contents.filter(user=user)
        queryset = sorted(queryset, reverse=True, key=lambda instance: instance.created)
        return queryset