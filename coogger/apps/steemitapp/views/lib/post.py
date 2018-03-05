from steem import Steem
from steem.account import Account
from steem.post import Post
from steem.amount import Amount
from dateutil.parser import parse
from datetime import datetime, timedelta
from apps.steemitapp.views.lib.bot import steem

def pending_payout(username):
    context = {}
    for post in steem.get_blog(username, 500, 500):
        post = Post(post["comment"])
        if post.is_main_post() and post["author"] == username:
            if "1970-01-01 00:00:00" == str(post["last_payout"]):
                payout = Amount(post["pending_payout_value"]).amount
                if payout == 0:
                    payout = (Amount(post["total_payout_value"]).amount + Amount(post["curator_payout_value"]).amount)
                context[post.title] = payout * 0.56 * 0.5
    return context

def detail(full_address):
    detail = {}
    author,permlink = full_address.split("/")[4:]
    post = steem.get_content(author.replace("@",""), permlink)
    detail["payout"] = post["pending_payout_value"] * 0.56 * 0.5
    detail["net_votes"] = post["net_votes"]
    detail["votes"] = [i["voter"] for i in steem.get_active_votes(author.replace("@",""), permlink)]
    return detail
