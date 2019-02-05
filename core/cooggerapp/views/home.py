# django
from django.shortcuts import render
from django.db.models import Q
from django.contrib import messages
from django.urls import resolve
from django.conf import settings

# django class based
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# form
from core.cooggerapp.forms import ReportsForm

# models
from core.cooggerapp.models import Content, SearchedWords, ReportModel

# views
from core.cooggerapp.utils import paginator


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
        context["content"] = paginator(self.request, queryset)
        return context


class Feed(View):  # TODO:  must be done using steem js
    template_name = "card/blogs.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):  # TODO:  buradaki işlemin daha hızlı olanı vardır ya
        queryset = []
        for q in Content.objects.filter(status="approved"):
            if q.user.username in self.steem_following(username=request.user.username):
                queryset.append(q)
        info_of_cards = paginator(request, queryset)
        context = dict(
            content=info_of_cards,
        )
        if queryset == []:
            messages.error(request, "You do not follow anyone yet on coogger.")
        return render(request, self.template_name, context)

    def steem_following(self, username):  # TODO: fixed this section,limit = 100 ?
        STEEM = Steem(nodes=['https://api.steemit.com'])
        return [i["following"] for i in STEEM.get_following(username, 'abit', 'blog', limit=100)]


class Review(TemplateView):
    template_name = "card/blogs.html"

    def get_context_data(self, **kwargs):
        context = super(Review, self).get_context_data(**kwargs)
        q = Q(status="shared") | Q(status="changed")
        queryset = Content.objects.filter(q)
        context["content"] = paginator(self.request, queryset)
        return context


class Report(View):
    form_class = ReportsForm

    template_name = "home/report.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        report_form = self.form_class()
        context = dict(
            report_form=report_form,
            content_id=request.GET["content_id"],
        )
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        report_form = self.form_class(request.POST)
        if report_form.is_valid():
            content = Content.objects.filter(id=request.POST["content_id"])[0]
            if ReportModel.objects.filter(user=request.user, content=content).exists():
                messages.error(request, "Your complaint is in the evaluation process.")
                return HttpResponseRedirect("/")
            report_form = report_form.save(commit=False)
            report_form.user = request.user
            report_form.content = content
            report_form.save()
            messages.error(request, "Your complaint has been received.")
            return HttpResponseRedirect("/")
        return HttpResponse(self.get(request, *args, **kwargs))


class Search(TemplateView):
    template_name = "card/blogs.html"

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context["content"] = paginator(self.request, self.search_algorithm())
        return context

    def get_form_data(self, name="query"):
        name = self.request.GET[name].lower()
        SearchedWords(word=name).save()
        return name

    def search_algorithm(self):
        searched_data = self.get_form_data()
        q = Q(title__contains=searched_data) | Q(topic__contains=searched_data) | Q(content__contains=searched_data)
        queryset = Content.objects.filter(q, status="approved").order_by("-views")
        return queryset
