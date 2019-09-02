from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import resolve, reverse
from django.views import View
from django.views.generic import TemplateView

from ..forms import ReportsForm
from ..models import Content, Issue, ReportModel, SearchedWords, Topic
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
        context["queryset"] = self.get_queryset()
        context["sort_topics"] = self.sort_topics()  # TODO just pc
        context["issues"] = Issue.objects.filter(status="open")[: settings.PAGE_SIZE]
        context["insection_left"] = True
        context["insection_right"] = True
        return context

    @staticmethod
    def sort_topics():
        topics = list()
        for topic in Topic.objects.all():
            if (topic not in topics) and (len(topics) <= 30) and (not topic.editable):
                topics.append(topic)
        return topics

    def get_queryset(self):
        if not self.is_authenticated and self.url_name == "home":
            how_many = 3 * 8
            queryset = User.objects.all().order_by("-date_joined")[:how_many]
            return paginator(self.request, queryset, how_many)
        else:
            queryset = Content.objects.filter(status="ready")
            return paginator(self.request, queryset)

    def get_template_names(self):
        if not self.is_authenticated and self.url_name == "home":
            return [self.introduction_template_name]
        else:
            return [self.template_name]




class Report(LoginRequiredMixin, View):
    form_class = ReportsForm
    template_name = "home/report.html"

    def get(self, request, content_id, *args, **kwargs):
        if request.is_ajax():
            report_form = self.form_class()
            context = dict(report_form=report_form, content_id=content_id)
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
    content_search_template_name = "home/search/content.html"
    user_search_template_name = "home/search/user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["queryset"] = paginator(
            self.request, self.get_queryset(), self.get_how_many()
        )
        return context

    def get_queryset(self):
        name = self.request.GET["query"].lower()
        SearchedWords(word=name).save()
        if name.startswith("@"):
            name = name[1:]
            return User.objects.filter(
                Q(username__contains=name)
                | Q(first_name__contains=name)
                | Q(last_name__contains=name)
            )
        return Content.objects.filter(Q(title__contains=name) & Q(status="ready"))

    def get_template_names(self):
        name = self.request.GET["query"].lower()
        if name.startswith("@"):
            return [self.user_search_template_name]
        return [self.content_search_template_name]

    def get_how_many(self):
        name = self.request.GET["query"].lower()
        if name.startswith("@"):
            return 30
        return settings.PAGE_SIZE


class Feed(Home):
    # TODO this class must be improved
    # make a new model for this op
    template_name = "card/blogs.html"

    def get_context_data(self, username, **kwargs):
        self.username = username
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        following = list(
            get_object_or_404(User, username=self.username).follow.following.all()
        )
        queryset = list()
        contents = Content.objects.filter(status="ready")
        for user in following:
            queryset += contents.filter(user=user)
        return paginator(
            self.request,
            sorted(
                queryset,
                reverse=True,
                key=lambda instance: instance.created
            ),
        )
