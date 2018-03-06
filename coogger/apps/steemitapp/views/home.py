#django
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.db.models import F
from django.contrib import messages as ms

# class
from django.views.generic.base import TemplateView

# views
from apps.steemitapp.views.lib.bot import SteemitBot

# models
from apps.steemitapp.models import SearchedWords

class Home(TemplateView):
    template_name = "apps/steemitapp/home/home.html"

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
        bot = SteemitBot(self.username)
        check_username = bot.check_username()
        context = super(Search, self).get_context_data(**kwargs)
        context["search"] = True
        if check_username is not None :
            context["check_username"] = check_username
            return context
        SearchedWords(word = self.username).save()
        context["follow"] = bot.follow()
        context["payout"] = bot.payout()
        context["price"] = bot.price()
        context["transfer"] = bot.transfer()
        context["account"] = bot.get_account_info()
        context["head"] = self.set_head()
        return context

    def set_head(self):
        html_head = dict(
         title = "{} steemitapp | coogger".format(self.username),
         keywords = "{} steemit,steem,steemapp,steemit search,coogger app,coogger apps,".format(self.username),
         description = "steemitapp search results of the Steemit user {}'s".format(self.username)
        )
        return html_head
