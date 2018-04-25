#django
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.db.models import Q
from django.contrib import messages as ms
from django.contrib.auth.models import User

#django class based
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

#form
from apps.cooggerapp.forms import ReportsForm

#models
from apps.cooggerapp.models import Content, SearchedWords, ReportModel, Following, OtherInformationOfUsers
from social_django.models import UserSocialAuth

#views
from apps.cooggerapp.views.tools import paginator

import json
from sc2py.sc2py import Sc2

#steem
from steem.post import Post
from steem.amount import Amount

class Home(TemplateView):
    template_name = "apps/cooggerapp/card/blogs.html"
    queryset = Content.objects.filter(status = "approved")

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context["content"] = paginator(self.request,self.queryset)
        return context

class Upvote(View):

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        user = request.POST["user"]
        permlink = request.POST["permlink"]
        weight = OtherInformationOfUsers.objects.filter(user = request.user)[0].vote_percent
        try:
            self.get_sc2(request).vote(voter = request.user.username, author = user, permlink = permlink, weight = int(weight))
            return HttpResponse(json.dumps({"upvote":True,"payout":self.get_payout(user,permlink)}))
        except Exception as e :
            return HttpResponse(json.dumps({"upvote":False,"error":str(e)}))

    def get_sc2(self, request):
        access_token = UserSocialAuth.objects.filter(uid = request.user)[0].extra_data["access_token"]
        return Sc2(str(access_token))

    @staticmethod
    def get_payout(user,permlink):
        def pending_payout(post):
            payout = Amount(post.pending_payout_value).amount
            if payout == 0:
                payout = (Amount(post.total_payout_value).amount + Amount(post.curator_payout_value).amount)
            return payout
        get_absolute_url = "@"+user+"/"+permlink
        post = Post(post = get_absolute_url)
        payout = round(pending_payout(post),4)
        return payout

class Feed(View):
    template_name = "apps/cooggerapp/card/blogs.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs): # TODO:  buradaki işlemin daha hızlı olanı vardır ya
        oof = []
        queryset = []
        for i in Following.objects.filter(user = request.user):
            i_wuser = i.which_user
            oof.append(i.which_user)
        for q in Content.objects.filter(status = "approved"):
            if q.user in oof:
                queryset.append(q)
        info_of_cards = paginator(request,queryset)
        context = dict(
        content = info_of_cards,
        )
        return render(request, self.template_name, context)

class Review(View):
    template_name = "apps/cooggerapp/card/blogs.html"

    def get(self, request, *args, **kwargs): # TODO:  buradaki işlemin daha hızlı olanı vardır ya
        queryset = Content.objects.filter(status = "shared")
        info_of_cards = paginator(request,queryset)
        context = dict(
        content = info_of_cards,
        )
        return render(request, self.template_name, context)

class Search(TemplateView):
    template_name = "apps/cooggerapp/card/blogs.html"

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context["content"] = paginator(self.request,self.get_queryset())
        return context

    def get_form_data(self,name = "query"):
        name = self.request.GET[name].lower()
        SearchedWords(word = name).save()
        return name

    def search_algorithm(self):
        searched_data = self.get_form_data()
        q = Q(title__contains = searched_data) | Q(content_list__contains = searched_data) | Q(content__contains = searched_data)
        queryset = Content.objects.filter(q,status = "approved").order_by("-views")
        return queryset

    def get_queryset(self):
        queryset = self.search_algorithm()
        return queryset

class Report(View):
    form_class = ReportsForm

    template_name = "apps/cooggerapp/home/report.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        report_form = self.form_class()
        context = dict(
        report_form = report_form,
        content_id = request.GET["content_id"],
        )
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        report_form = self.form_class(request.POST)
        if report_form.is_valid():
            content = Content.objects.filter(id = request.POST["content_id"])[0]
            if ReportModel.objects.filter(user = request.user,content = content).exists():
                ms.error(request,"Your complaint is in the evaluation process.")
                return HttpResponseRedirect("/")
            report_form  = report_form.save(commit=False)
            report_form.user = request.user
            report_form.content = content
            report_form.save()
            ms.error(request,"Your complaint has been received.")
            return HttpResponseRedirect("/")
        return HttpResponse(self.get(request, *args, **kwargs))
