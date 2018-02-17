#django
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.db.models import F
from django.contrib import messages as ms

# class
from django.views.generic.base import TemplateView

# views
from apps.steemitapp.views.bot import SteemitBot

# models
from apps.steemitapp.models import SearchedWords

class Home(TemplateView):
    template_name = "apps/steemitapp/home/home.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        return context

class Search(Home):

    def get_context_data(self, **kwargs):
        username = self.request.GET["username"]
        bot = SteemitBot(username)
        check_username = bot.check_username()
        context = super(Search, self).get_context_data(**kwargs)
        if check_username is not None :
            context["check_username"] = check_username
            return context
        SearchedWords(word = username).save()
        follow = bot.follow()
        payout = bot.payout()
        transfer = bot.transfer()
        context["search"] = True
        context["follower_count"] = follow[0]
        context["following_count"] = follow[1]
        context["d_follow"] = follow[2]
        context["d_following"] = follow[3]
        context["payout"] = payout[1:]
        context["post_payout"] = payout[0]
        context["price"] = bot.price()
        context["account"] = transfer[0]
        context["total"] = transfer[1]
        context["change_rate"] = transfer[2]
        return context
