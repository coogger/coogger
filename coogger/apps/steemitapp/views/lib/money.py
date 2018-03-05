# steem
from steem.steemd import Steemd
from apps.steemitapp.views.lib.bot import steem

# bot
from apps.steemitapp.views.lib.post import pending_payout

# py
import json
import requests

def price():
    "https://min-api.cryptocompare.com/data/price?fsym=USD&tsyms=BTC,USD,SBD,STEEM"

    btc_api = "https://api.coinmarketcap.com/v1/ticker/bitcoin/"
    ltc_api = "https://api.coinmarketcap.com/v1/ticker/litecoin/"
    steem_api = "https://api.coinmarketcap.com/v1/ticker/steem/"
    sbd_api = "https://api.coinmarketcap.com/v1/ticker/steem-dollars/"
    steem_sbd_api = "https://min-api.cryptocompare.com/data/price?fsym=STEEM&tsyms=SBD"
    coins = {}
    for r_api in [btc_api,ltc_api,steem_api,sbd_api]:
        coin_info = json.loads(requests.get(r_api).text)
        coins[coin_info[0]["symbol"]] = coin_info[0]["price_usd"]
    steem_sbd = json.loads(requests.get(steem_sbd_api).text)
    coins["SBD-STEEM"] = steem_sbd["SBD"]
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
        val = val[0]+"."+val[1][:6]
        return float(val)
