#django
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.db.models import F
from django.contrib import messages as ms
from django.views.generic.base import TemplateView

from easysteem.easysteem import Blocktrades
from easysteem.easysteem import Binance as easybinance
from easysteem.easysteem import EasyPost
from easysteem.easysteem import Oogg
price = Oogg.price()

# python
import requests
import json

class Koinim(TemplateView):
    template_name = "home/home.html"

    def __init__(self):
        btc_to_try_api = "https://koinim.com/ticker/"
        r = requests.get(btc_to_try_api).text
        self.j = json.loads(r)

    def get_context_data(self, **kwargs):
        BTC = self.calculate_btc()
        TRY = BTC * self.buy() - 3
        context = super(Koinim, self).get_context_data(**kwargs)
        context["BTC"] = round(BTC,4)
        context["TRY"] = round(TRY,4)
        context["change_rate"] = self.change_rate()
        context["head"] = self.set_head()
        return context

    @staticmethod
    def set_head():
        html_head = dict(
         title = "steemitapp convert | coogger",
         keywords = "sbd convert,steem convert,sbd convert try,steem convert try,bitcoin convert",
         description = "steemitapp convert results of from sbd ,steem or bitcoin to try"
        )
        return html_head

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

    def sell(self):
        return float(self.j["sell"])

    def buy(self):
        return float(self.j["buy"])

    def change_rate(self):
        return float(self.j["change_rate"])

class Binance(Koinim):

    def get_context_data(self, **kwargs):
        context = super(Binance, self).get_context_data(**kwargs)
        return context

    @staticmethod
    def set_head():
        html_head = dict(
         title = "Convert STEEM from binance to koinim.com to TRY | coogger",
         keywords = "steem convert,steem convert try,",
         description = "steemitapp convert results of from steem to try on binance and koinim"
        )
        return html_head

    def get_name(self):
        try:
            return self.request.GET["get_binance_steem"],"steem"
        except KeyError:
            return self.request.GET["get_binance_sbd"],"sbd"

    def calculate_btc(self):
        name = self.get_name()
        if name[1] == "steem":
            return easybinance().steem_to_btc(name[0])
        elif name[1] == "sbd":
            return easybinance().sbd_to_steem_to_btc(name[0])
