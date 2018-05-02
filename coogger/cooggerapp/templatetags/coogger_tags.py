from django import template
register = template.Library()

# steem
from easysteem.easysteem import Oogg

@register.filter(name="upvote")
def upvote(value, arg):# kullanıcı upvote atmış mı atmamışmı
    try:
        voters = Oogg(node = None).voters(value.user.username,value.permlink)
    except:
        return None
    if arg in voters:
        return True
    return False

@register.filter(name="percent")
def percent(value, arg):
    return int(value/100)
