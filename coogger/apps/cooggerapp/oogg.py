# django
from django.utils.text import slugify

# python
import requests
import re
import json

#steem
from steem.steem import Commit
from steem.post import Post
from steem.amount import Amount
from steem import Steem

class Oogg:

    @staticmethod
    def reply(title, body, author, identifier):
        Commit(steem = STEEM).post(
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
    def get_steem(key):
        return Steem(nodes=['https://api.steemit.com'],keys = [key])

    @staticmethod
    def get_account_info(username):
        get_account = Steem().get_account(username)
        get_account = json.loads(get_account["json_metadata"])
        try:
            context = get_account["profile"]
            return context
        except:
            return False

    @staticmethod
    def follow_count(username):
        follow_count = Steem().get_follow_count(username)
        return follow_count

    @staticmethod
    def post_reward(queryset):
        for q in queryset:
            title = slugify(q.title.lower(), allow_unicode=True)
            try:
                post = Post(post = q.user.username+"/"+title)
            except:
                break
            pp = Oogg.pending_payout(post)
            identifier = post.identifier
            yield dict(
            identifier = pp
            )

    @staticmethod
    def calculate_sbd_sp(payout):
        return dict(
        total = round(payout,4),
        sp = round(payout * 0.15,4),
        sbd = round(payout * 0.75/2,4),
        )

    @staticmethod
    def pending_payout(post):
        payout = Amount(post.pending_payout_value).amount
        if payout == 0:
            payout = (Amount(post.total_payout_value).amount + Amount(post.curator_payout_value).amount)
        return Oogg.calculate_sbd_sp(payout)
