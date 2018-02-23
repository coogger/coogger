#django
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.db.models import F
from django.contrib import messages as ms
from django.views.generic.base import TemplateView

# views
from apps.steemitapp.views.lib.transfer import Blocktrades
from apps.steemitapp.views.lib.money import Pending
float_to_flot = Pending.float_to_flot

# python
import requests
import json

# binance api
from binance.client import Client

class Koinim(TemplateView):
    template_name = "apps/steemitapp/home/home.html"

    def __init__(self):
        btc_to_try_api = "https://koinim.com/ticker/"
        r = requests.get(btc_to_try_api).text
        self.j = json.loads(r)

    def get_context_data(self, **kwargs):
        BTC = self.calculate_btc()
        TRY = BTC * self.buy()
        context = super(Koinim, self).get_context_data(**kwargs)
        html_head = dict(
         title = "steemitapp convert | coogger",
         keywords = "sbd convert,steem convert,sbd convert try,steem convert try,bitcoin convert",
         description = "steemitapp convert results of from sbd ,steem or bitcoin to try"
        )
        context["head"] = html_head
        context["BTC"] = float_to_flot(BTC)
        context["TRY"] = float_to_flot(TRY)
        context["change_rate"] = self.change_rate()
        return context

    def get_name(self):
        try:
            return self.request.GET["get_sbd"],"sbd"
        except KeyError:
            try:
                return self.request.GET["get_steem"],"steem"
            except KeyError:
                return self.request.GET["get_btc"],"btc"

    def calculate_btc(self):
        # This function calculates value of how many btc from sbd or steem on Blocktrades
        name = self.get_name()
        if name[1] == "sbd":
            return Blocktrades.amount(float(name[0]))
        elif name[1] == "steem":
            return Blocktrades.amount_of_steem(float(name[0]))
        elif name[1] == "btc":
            return float(name[0])

    #def sell(self):
        #return float(self.j["sell"])

    def buy(self):
        return float(self.j["buy"])

    def change_rate(self):
        return float(self.j["change_rate"])

class Binance(Koinim):

    def get_context_data(self, **kwargs):
        context = super(Binance, self).get_context_data(**kwargs)
        html_head = dict(
         title = "Convert STEEM from binance to koinim.com to TRY | coogger",
         keywords = "steem convert,steem convert try,",
         description = "steemitapp convert results of from steem to try on binance and koinim"
        )
        return context

    def get_name(self):
        return self.request.GET["get_binance_steem"]

    def calculate_btc(self):
        # This function calculates value of how many btc from sbd or steem on Blocktrades
        name = float(self.get_name())
        binance_client = Client("Id2J31MWY7Sb0dsqzFbp8k0f2RnJa58Pwt2Qdy1VFUe96mfc9bG9F8PfmE0fQAYW", "6o4GNYxwCjDepuipegYwgMhQJISZ3QMzZTaDdE8pZ3GedH0yqzmIebAc7qJp7OsQ")
        binance_client = binance_client.get_all_tickers()
        for i in binance_client:
            if i["symbol"] == "STEEMBTC":
                price = i["price"]
                return float(price) * name
