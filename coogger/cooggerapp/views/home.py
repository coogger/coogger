# django
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.db.models import Q
from django.contrib import messages as ms
from django.contrib.auth.models import User

# django class based
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# form
from cooggerapp.forms import ReportsForm

# models
from cooggerapp.models import Content, SearchedWords, ReportModel, OtherInformationOfUsers
from steemconnect_auth.models import Community

# views
from cooggerapp.views.tools import paginator

import json

# steem
from steem import Steem
from steem.post import Post
from steem.amount import Amount


class Home(TemplateView):
    template_name = "card/blogs.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        if self.request.community_model.name == "coogger":
            queryset = Content.objects.filter(status="approved")
        else:
            queryset = Content.objects.filter(community=self.request.community_model, status="approved")
        context["content"] = paginator(self.request, queryset)
        return context


class Feed(View):  # TODO:  sorunlu
    template_name = "card/blogs.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):  # TODO:  buradaki işlemin daha hızlı olanı vardır ya
        queryset = []
        for q in Content.objects.filter(community=request.community_model, status="approved"):
            if q.user.username in self.steem_following(username=request.user.username):
                queryset.append(q)
        info_of_cards = paginator(request, queryset)
        context = dict(
            content=info_of_cards,
        )
        if queryset == []:
            ms.error(request, "You do not follow anyone yet on {}.".format(request.community_model.name))
        return render(request, self.template_name, context)

    def steem_following(self, username):  # TODO: fixed this section,limit = 100 ?
        STEEM = Steem(nodes=['https://api.steemit.com'])
        return [i["following"] for i in STEEM.get_following(username, 'abit', 'blog', limit=100)]


class Review(View):
    template_name = "card/blogs.html"

    def get(self, request, *args, **kwargs):
        # TODO:  buradaki işlemin daha hızlı olanı vardır ya
        q = Q(status="shared") | Q(status="changed")
        if self.request.community_model.name == "coogger":
            queryset = Content.objects.filter(q)
        else:
            queryset = Content.objects.filter(q).filter(community=request.community_model)
        info_of_cards = paginator(request, queryset)
        context = dict(
            content=info_of_cards,
        )
        return render(request, self.template_name, context)


class Search(TemplateView):
    template_name = "card/blogs.html"

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context["content"] = paginator(self.request, self.get_queryset())
        return context

    def get_form_data(self, name="query"):
        name = self.request.GET[name].lower()
        SearchedWords(word=name).save()
        return name

    def search_algorithm(self):
        searched_data = self.get_form_data()
        q = Q(title__contains=searched_data) | Q(topic__contains=searched_data) | Q(content__contains=searched_data)
        if self.request.community_model.name == "coogger":
            queryset = Content.objects.filter(q, status="approved").order_by("-views")
        else:
            queryset = Content.objects.filter(q, community=self.request.community_model, status="approved").order_by("-views")
        return queryset

    def get_queryset(self):
        queryset = self.search_algorithm()
        return queryset


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
                ms.error(request, "Your complaint is in the evaluation process.")
                return HttpResponseRedirect("/")
            report_form = report_form.save(commit=False)
            report_form.user = request.user
            report_form.content = content
            report_form.save()
            ms.error(request, "Your complaint has been received.")
            return HttpResponseRedirect("/")
        return HttpResponse(self.get(request, *args, **kwargs))


class Communities(TemplateView):
    template_name = "home/communities.html"

    def get_context_data(self, **kwargs):
        context = super(Communities, self).get_context_data(**kwargs)
        queryset = Community.objects.filter(active=True)
        context["communities"] = queryset
        return context

class Supporters(TemplateView):
    template_name = "home/supporters.html"
