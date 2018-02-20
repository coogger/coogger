#django
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.db.models import F
from django.contrib import messages as ms

# class
from django.views.generic.base import TemplateView

# views
from apps.steemitapp.views.transfer import Blocktrades,Koinim
from apps.steemitapp.views.money import Pending

float_to_flot = Pending.float_to_flot

class SbdTry(TemplateView):
    template_name = "apps/steemitapp/home/home.html"

    def get_context_data(self, **kwargs):
        get_sbd = self.request.GET["get_sbd"]
        BTC = Blocktrades.amount(float(get_sbd))
        TRY = BTC * Koinim().buy()
        context = super(SbdTry, self).get_context_data(**kwargs)
        html_head = dict(
         title = "steemitapp convert | coogger",
         keywords = "sbd convert,steem convert,sbd convert try,steem convert try",
         description = "steemitapp convert results of from sbd to try"
        )
        context["convert_sbd_try"] = True
        context["head"] = html_head
        context["BTC"] = float_to_flot(BTC)
        context["TRY"] = float_to_flot(TRY)
        return context

class SteemTry(TemplateView):
    template_name = "apps/steemitapp/home/home.html"

    def get_context_data(self, **kwargs):
        get_steem = self.request.GET["get_steem"]
        BTC = Blocktrades.amount_of_steem(float(get_steem))
        TRY = BTC * Koinim().buy()
        context = super(SteemTry, self).get_context_data(**kwargs)
        html_head = dict(
         title = "steemitapp convert | coogger",
         keywords = "sbd convert,steem convert,sbd convert try,steem convert try",
         description = "steemitapp convert results of from steem to try"
        )
        context["convert_steem_try"] = True
        context["head"] = html_head
        context["BTC"] = float_to_flot(BTC)
        context["TRY"] = float_to_flot(TRY)
        return context
