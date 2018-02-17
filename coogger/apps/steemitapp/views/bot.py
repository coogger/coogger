# steemit
from steem import Steem
steem = Steem()

# python
import requests
import re
import json

# bot
from apps.steemitapp.views.post import detail
from apps.steemitapp.views.money import Pending,price
from apps.steemitapp.views.transfer import Blocktrades,Koinim


class Text:
    def __init__(self):
        self.text_check_username = "Make sure you write the correct {} user is not on steemit.com"
        self.text_sbd = "{} amount of sbd in account {}"
        self.text_price = "BTC : {} USD","LTC : {} USD","SBD : {} USD","STEEM : {} USD"
        self.text_post = "pending payout value : {}\nnet_votes : {}\nvotes : {}\n"

class SteemitBot(Text):

    def __init__(self, username):
        super(SteemitBot, self).__init__()
        self.username = username

    def post_detail(self, full_address):
        detail = detail(full_address)
        return self.text_post.format(detail["payout"],detail["net_votes"],detail["votes"])

    def check_username(self):
        if steem.lookup_account_names([self.username]) == [None]:
            return self.text_check_username.format(self.username)

    def follow(self):
        list_followers = [] # seni takip edenler
        list_following = [] # senin takip ettklerin
        d_follow = []       # seni takip etmeyenler
        d_following = []    # senin takip ettiklerin
        get_followers = steem.get_followers(self.username, 'abit', 'blog', 1000)
        get_following = steem.get_following(self.username, 'abit', 'blog', 100)
        follow_count = steem.get_follow_count(self.username)
        follower_count = follow_count["follower_count"]
        following_count = follow_count["following_count"]
        for i in get_followers:
            list_followers.append(i["follower"])
        for i in get_following:
            list_following.append(i["following"])
        for i in list_following:
            if i not in list_followers:
                d_follow.append(i)
        for i in list_followers:
            if i not in list_following:
                d_following.append(i)
        return follower_count,following_count,d_follow,d_following

    def price(self):
        coin = price()
        return "BTC : {} USD".format(coin["BTC"]),"LTC : {} USD".format(coin["LTC"]),"SBD : {} USD".format(coin["SBD"]),"STEEM : {} USD".format(coin["STEEM"])

    def payout(self):
        payout_info = Pending(self.username)
        sbd_in_account = str(payout_info.sbd_in_account)
        usd_in_account = str(payout_info.usd_in_account)
        total_sbd = str(payout_info.total_sbd)
        total_usd = str(payout_info.total_usd)
        sbd_in_account = "Amount of SBD in your account {} $".format(sbd_in_account)
        usd_in_account = "Amount of USD in your account {} $".format(usd_in_account)
        total_sbd = "Total SBD from in your account {} $".format(total_sbd)
        total_usd = "Total USD from in your account {} $".format(total_usd)
        posts = []
        money_title = payout_info.posts
        for i in money_title:
            posts.append((i,money_title[i]))
        return posts,sbd_in_account,usd_in_account,total_sbd,total_usd

    def transfer(self):
        b = Blocktrades(self.username)
        k = Koinim
        sell = k.sell
        change_rate = k.change_rate
        account = Pending.float_to_flot(b.account() * sell)
        total = Pending.float_to_flot(b.total() * sell)
        return account, total, change_rate
