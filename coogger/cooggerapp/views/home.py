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
from cooggerapp.forms import ReportsForm

#models
from cooggerapp.models import Content, SearchedWords, ReportModel, OtherInformationOfUsers,Community

#views
from cooggerapp.views.tools import paginator,get_community_model

import json
# sc2py.
from sc2py.sc2py import Sc2
from sc2py.operations import Operations
from sc2py.operations import Vote

#steem
from steem.post import Post
from steem.amount import Amount

# easysteem
from easysteem.easysteem import EasyFollow

class Home(TemplateView):
    template_name = "card/blogs.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        community_model = get_community_model(self.request)
        context["community"] = community_model
        queryset = Content.objects.filter(community = community_model,status = "approved")
        context["content"] = paginator(self.request,queryset)
        return context

class Upvote(View):

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        user = request.POST["user"]
        permlink = request.POST["permlink"]
        weight = OtherInformationOfUsers.objects.filter(user = request.user)[0].vote_percent
        try:
            vote_json = Vote(voter = request.user.username, author = user, permlink = permlink, weight = int(weight)).json
            op = Operations(json = vote_json).json
            Sc2(token = self.get_access_token(request),data = op).run
            return HttpResponse(json.dumps({"upvote":True,"payout":self.get_payout(user,permlink)}))
        except Exception as e :
            return HttpResponse(json.dumps({"upvote":False,"error":str(e)}))

    def get_access_token(self, request):
        access_token = SteemConnectUser.objects.filter(user = request.user)[0].access_token
        return str(access_token)

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
    template_name = "card/blogs.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs): # TODO:  buradaki işlemin daha hızlı olanı vardır ya
        oof = []
        queryset = []
        ef = EasyFollow(username = request.user.username)
        for which_user in ef.following():
            oof.append(which_user)
        community_model = get_community_model(request)
        for q in Content.objects.filter(community = community_model,status = "approved"):
            if q.user.username in oof:
                queryset.append(q)
        info_of_cards = paginator(request,queryset)
        context = dict(
        content = info_of_cards,
        community = community_model,
        )
        if queryset == []:
            ms.error(request,"You do not follow anyone yet on {}.".format(community_model.name))
        return render(request, self.template_name, context)

class Review(View):
    template_name = "card/blogs.html"

    def get(self, request, *args, **kwargs): # TODO:  buradaki işlemin daha hızlı olanı vardır ya
        community_model = get_community_model(request)
        q = Q(status = "shared") | Q(status = "changed")
        queryset = Content.objects.filter(q).filter(community = community_model)
        info_of_cards = paginator(request,queryset)
        context = dict(
        content = info_of_cards,
        community = community_model,
        )
        return render(request, self.template_name, context)

class Search(TemplateView):
    template_name = "card/blogs.html"

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context["content"] = paginator(self.request,self.get_queryset())
        context["community"] = self.community_model
        return context

    def get_form_data(self,name = "query"):
        name = self.request.GET[name].lower()
        SearchedWords(word = name).save()
        return name

    def search_algorithm(self):
        searched_data = self.get_form_data()
        self.community_model = get_community_model(self.request)
        q = Q(title__contains = searched_data) | Q(topic__contains = searched_data) | Q(content__contains = searched_data)
        queryset = Content.objects.filter(q,community = self.community_model,status = "approved").order_by("-views")
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
