# python
import requests
import json

# bot
from apps.steemitapp.views.lib.money import Pending

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

    @staticmethod
    def amount_of_steem(steem = 1):
        sbd_to_btc_api = "https://blocktrades.us/api/v2/estimate-output-amount?inputAmount={}&inputCoinType=steem&outputCoinType=btc".format(steem)
        r = requests.get(sbd_to_btc_api).text
        j = json.loads(r)
        return float(j["outputAmount"])
