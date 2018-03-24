# python
import requests
import re
import json
from datetime import datetime

#steem
from steem.steem import Commit
from steem.post import Post
from steem.amount import Amount
from steem import Steem
STEEM = Steem(nodes=['https://api.steemit.com'])


class Oogg:

    def sbd(self, username):
        return STEEM.get_account(username)['sbd_balance']

    @staticmethod
    def price():
        btc_api = "https://api.coinmarketcap.com/v1/ticker/bitcoin/"
        ltc_api = "https://api.coinmarketcap.com/v1/ticker/litecoin/"
        steem_api = "https://api.coinmarketcap.com/v1/ticker/steem/"
        sbd_api = "https://api.coinmarketcap.com/v1/ticker/steem-dollars/"
        ethereum = "https://api.coinmarketcap.com/v1/ticker/ethereum/"
        coins = {}
        for r_api in [btc_api,ltc_api,steem_api,sbd_api,ethereum]:
            coin_info = json.loads(requests.get(r_api).text)
            coins[coin_info[0]["symbol"]] = coin_info[0]["price_usd"]
        return coins

    def transfer(self, username):
        b = Blocktrades(username)
        k = Koinim()
        buy = k.buy()
        hmuch_btc_in_account = b.account()
        change_rate = k.change_rate()
        hmuch_try = hmuch_btc_in_account * buy
        if hmuch_try > 3:
            hmuch_try = hmuch_try - 3
        total = b.total() * buy
        return hmuch_btc_in_account,hmuch_try, round(total,6), change_rate


    @staticmethod
    def voters(identify):
        author,permlink = identify.split("/")[4:]
        return [i["voter"] for i in STEEM.get_active_votes(author.replace("@",""), permlink)]

    @staticmethod
    def reply(title, body, author, identifier):
        Commit(steem=STEEM).post(
        title = title,
        body = body,
        author = author,
        permlink = None,
        reply_identifier = identifier,
        json_metadata = None,
        comment_options = None,
        community = None,
        tags = None,
        beneficiaries = None,
        self_vote = False
        )

    @staticmethod
    def post(title, body, author,tags, identifier):
        Commit(steem=STEEM).post(
        title = title,
        body = body,
        author = author,
        permlink = None,
        reply_identifier = None,
        json_metadata = None,
        comment_options = None,
        community = None,
        tags = tags,
        beneficiaries = None,
        self_vote = False
        )

    @staticmethod
    def get_replies_list(post):
        return [str(i.author) for i in post.get_replies()]

class EasyFollow:

    def __init__(self,username):
        self.username = username

    def followers(self):
        return [i["follower"] for i in STEEM.get_followers(self.username, 'abit', 'blog',limit = 1000)]

    def following(self):
        return [i["following"] for i in STEEM.get_following(self.username, 'abit', 'blog',limit = 100)]

    def not_follow_you(self): # beni takip etmeyenler
        return set(self.followers()) - set(self.following())

    def not_follow(self): # benim takip etmediklerim
        return set(self.following()) - set(self.followers())

    def get_follower_count(self):
        return self.follow_cout()["follower_count"]

    def get_following_count(self):
        return self.follow_cout()["following_count"]

    def follow_cout(self):
        return STEEM.get_follow_count(self.username)


class EasyAccount:
    def __init__(self,username):
        self.username = username
        self.price_sbd = float(price()["SBD"])
        self.sbd_in_account = Amount(STEEM.get_account(username)['sbd_balance']).amount
        self.usd_in_account = self.sbd_in_account * self.price_sbd

    def total_sbd(self):
        total_sbd = self.sbd_in_account
        for pp in PostDetail.pending_payout(self.username):
            total_sbd += pp["sbd"]
        return total_sbd


class PostDetail:

    @staticmethod
    def pending_payout(username):
        for post in STEEM.get_blog(username, 0, 500):
            post = Post(post["comment"])
            if post.is_main_post() and post.author == username:
                if datetime(1970, 1, 1, 0, 0) == post.last_payout:
                    payout = Amount(post.pending_payout_value).amount
                    if payout == 0:
                        payout = (Amount(post.total_payout_value).amount + Amount(post.curator_payout_value).amount)
                    yield dict(
                    title = post.title,
                    payout = round(payout,4),
                    sp = round(payout*0.15,4),
                    sbd = round(payout*0.75/2,4),
                    )
                else:
                    break

    @staticmethod
    def votes_by_rshares(url):
        author,permlink = url.split("/")[4:]
        identify = author+"/"+permlink
        reward_fund = STEEM.get_reward_fund()
        reward_balance = Amount(reward_fund["reward_balance"]).amount
        recent_claims = float(reward_fund["recent_claims"])
        reward_share = reward_balance / recent_claims
        base = Amount(STEEM.get_current_median_history_price()["base"]).amount
        post = Post(identify)
        votes = []
        for vote in post["active_votes"]:
            if len(votes) < 30:
                votes.append(vote)
            else:
                break
        for vote in sorted(votes, key = lambda x: float(x["rshares"]), reverse=True):
            rshares = float(vote["rshares"]) * reward_share * base
            sbd_sp = PostDetail.calculate_sbd_sp(rshares)
            if rshares != 0:
                yield dict(
                voter = vote["voter"],
                rshares = round(rshares,4),
                percent = vote["percent"] / 100,
                sp = sbd_sp["sp"],
                sbd = sbd_sp["sbd"],
                )

    @staticmethod
    def calculate_sbd_sp(payout):
        return dict(
        sp = round(payout * 0.15,4),
        sbd = round(payout * 0.75/2,4),
        )


class Koinim():

    def __init__(self):
        btc_to_try_api = "https://koinim.com/ticker/"
        r = requests.get(btc_to_try_api).text
        self.j = json.loads(r)

    def sell(self):
        return float(self.j["sell"])

    def buy(self):
        return float(self.j["buy"])

    def change_rate(self):
        return float(self.j["change_rate"])


class Blocktrades(EasyAccount):

    def account(self):
        Amount = self.amount(sbd = self.sbd_in_account)
        return Amount

    def total(self):
        Amount = self.amount(sbd = self.total_sbd())
        return Amount

    @staticmethod
    def amount(sbd = 1):
        sbd_to_btc_api = "https://blocktrades.us/api/v2/estimate-output-amount?inputAmount={}&inputCoinType=sbd&outputCoinType=btc".format(sbd)
        r = requests.get(sbd_to_btc_api).text
        j = json.loads(r)
        return float(j["outputAmount"])
