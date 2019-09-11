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
            queryset = User.objects.filter(is_active=True).order_by("-date_joined")[
                :how_many
            ]
            return paginator(self.request, queryset, how_many)
        else:
            queryset = Content.objects.filter(user__is_active=True, status="ready")
            return paginator(self.request, queryset)

    def get_template_names(self):
        if not self.is_authenticated and self.url_name == "home":
            return [self.introduction_template_name]
        else:
            return [self.template_name]


class Report(LoginRequiredMixin, View):
    form_class = ReportsForm
    template_name = "home/report.html"

    def get(self, request, content_id):
        if request.is_ajax():
            report_form = self.form_class()
            context = dict(report_form=report_form, content_id=content_id)
            return render(request, self.template_name, context)
        raise Http404

    def post(self, request, content_id):
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
        return HttpResponse(self.get(request, content_id))


class Search(Home):
    content_search_template_name = "home/search/content.html"
    user_search_template_name = "home/search/user.html"
    not_result_template_name = "home/search/not_result.html"
    is_queryset_exists = True
    page_size = settings.PAGE_SIZE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["queryset"] = self.get_queryset()[: self.page_size]
        return context

    def get_queryset(self):
        name = self.request.GET["query"].lower()
        SearchedWords(word=name).save()
        if name.startswith("@"):
            self.page_size = 30
            name = name[1:]
            queryset = User.objects.filter(
                Q(is_active=True),
                Q(username__contains=name)
                | Q(first_name__contains=name)
                | Q(last_name__contains=name),
            )
            self.is_queryset_exists = queryset.exists()
            return queryset
        queryset = Content.objects.filter(Q(title__contains=name) & Q(status="ready"))
        self.is_queryset_exists = queryset.exists()
        return queryset

    def get_template_names(self):
        if not self.is_queryset_exists:
            return [self.not_result_template_name]
        name = self.request.GET["query"].lower()
        if name.startswith("@"):
            return [self.user_search_template_name]
        return [self.content_search_template_name]


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
            sorted(queryset, reverse=True, key=lambda instance: instance.created),
        )
