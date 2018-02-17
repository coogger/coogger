# steem
from steem import Steem
steem = Steem()

# bot
from apps.steemitapp.views.post import pending_payout

# py
import json
import requests

def price():
    btc_api = "https://api.coinmarketcap.com/v1/ticker/bitcoin/"
    ltc_api = "https://api.coinmarketcap.com/v1/ticker/litecoin/"
    steem_api = "https://api.coinmarketcap.com/v1/ticker/steem/"
    sbd_api = "https://api.coinmarketcap.com/v1/ticker/steem-dollars/"
    coins = {}
    for r_api in [btc_api,ltc_api,steem_api,sbd_api]:
        coin_info = json.loads(requests.get(r_api).text)
        coins[coin_info[0]["symbol"]] = coin_info[0]["price_usd"]
    return coins

class Pending:
    def __init__(self,username):
        self.sbd_in_account = float(steem.get_account(username)['sbd_balance'].replace(" SBD",""))
        price_sbd = float(price()["SBD"])
        self.usd_in_account = self.float_to_flot(self.sbd_in_account * price_sbd)
        self.total_sbd = self.sbd_in_account
        pp = pending_payout(username)
        self.posts = {}
        for p in pp:
            money = self.float_to_flot(pp[p])
            title = p
            self.total_sbd += money
            self.posts[money] = title
        self.total_sbd = self.float_to_flot(self.total_sbd)
        self.total_usd = self.float_to_flot(self.total_sbd * price_sbd)

    @staticmethod
    def float_to_flot(val):
        val = str(val)
        val = val.split(".")
        val = val[0]+"."+val[1][:3]
        return float(val)
