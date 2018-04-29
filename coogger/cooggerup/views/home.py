#django
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.db.models import F
from django.contrib import messages as ms

# class
from django.views.generic.base import TemplateView

from easysteem.easysteem import EasyFollow
from easysteem.easysteem import EasyAccount
from easysteem.easysteem import EasyPost
from easysteem.easysteem import Oogg

# models
# from cooggerup.models import SearchedWords

class Home(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context["head"] = self.set_head()
        return context

    @staticmethod
    def set_head():
        html_head = dict(
         title = "steemitapp | coogger",
         keywords = "steem,steemapp,steemit,coogger app,coogger apps,",
         description = "steemitapp is a coogger application for steemit.com"
        )
        return html_head

class Search(Home):

    def get_username(self):
        self.username = self.request.GET["username"]

    def get_context_data(self, **kwargs):
        self.get_username()
        context = super(Search, self).get_context_data(**kwargs)
        context["search"] = True
        context["follow_info"] = EasyFollow(self.username)
        context["payout"] = EasyPost().pending_payout(self.username)
        context["price"] = Oogg.price()
        context["transfer"] = Oogg.transfer(self.username)
        context["account"] = EasyAccount(self.username)
        context["head"] = self.set_head()
        return context

    def set_head(self):
        html_head = dict(
         title = "{} steemitapp | coogger".format(self.username),
         keywords = "{} steemit,steem,steemapp,steemit search,coogger app,coogger apps,".format(self.username),
         description = "steemitapp search results of the Steemit user {}'s".format(self.username)
        )
        return html_head
