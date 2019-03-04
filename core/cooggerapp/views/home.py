# django
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from django.urls import resolve
from django.conf import settings
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# form
from core.cooggerapp.forms import ReportsForm

# models
from core.cooggerapp.models import Content, SearchedWords, ReportModel


class Home(TemplateView):
    template_name = "card/blogs.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        queryset = Content.objects.filter(status="approved")
        url_name = resolve(self.request.path_info).url_name
        is_authenticated = self.request.user.is_authenticated
        if not is_authenticated and url_name == "home":
            self.template_name = "home/introduction.html"
            check, posts = [], []
            for query in queryset:
                if query.user not in check:
                    check.append(query.user)
                    posts.append(query)
                if len(posts) == settings.PAGE_SIZE:
                    break
            context["introduction"] = True
            queryset = posts
        context["content"] = queryset[:settings.PAGE_SIZE]
        return context


class Review(TemplateView):
    template_name = "card/blogs.html"

    def get_context_data(self, **kwargs):
        context = super(Review, self).get_context_data(**kwargs)
        q = Q(status="shared") | Q(status="changed")
        queryset = Content.objects.filter(q)
        context["content"] = queryset[:settings.PAGE_SIZE]
        return context


class Report(LoginRequiredMixin, View):
    form_class = ReportsForm
    template_name = "home/report.html"

    def get(self, request, *args, **kwargs):
        report_form = self.form_class()
        context = dict(
            report_form=report_form,
            content_id=request.GET["content_id"],
        )
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        report_form = self.form_class(request.POST)
        if report_form.is_valid():
            content = Content.objects.filter(id=request.POST["content_id"])[0]
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


class Search(TemplateView):
    template_name = "card/blogs.html"

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context["content"] = self.search_algorithm()[settings.PAGE_SIZE]
        return context

    def get_form_data(self, name="query"):
        name = self.request.GET[name].lower()
        SearchedWords(word=name).save()
        return name

    def search_algorithm(self):
        searched_data = self.get_form_data()
        q = Q(title__contains=searched_data) | Q(topic__contains=searched_data) | Q(body__contains=searched_data)
        queryset = Content.objects.filter(q, status="approved").order_by("-views")
        return queryset
