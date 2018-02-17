# python
import requests
import json

# bot
from apps.steemitapp.views.money import Pending

class Koinim:
    btc_to_try_api = "https://koinim.com/ticker/"
    r = requests.get(btc_to_try_api).text
    j = json.loads(r)
    sell, buy, change_rate = float(j["sell"]),float(j["buy"]),float(j["change_rate"])

class Blocktrades(Pending):

    def account(self):
        Amount = self.amount(sbd = self.sbd_in_account)
        return Amount

    def total(self):
        Amount = self.amount(sbd = self.total_sbd)
        return Amount

    @staticmethod
    def amount(sbd = 1):
        sbd_to_btc_api = "https://blocktrades.us/api/v2/estimate-output-amount?inputAmount={}&inputCoinType=sbd&outputCoinType=btc".format(sbd)
        r = requests.get(sbd_to_btc_api).text
        j = json.loads(r)
        return float(j["outputAmount"])
