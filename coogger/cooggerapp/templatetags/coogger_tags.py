from django import template
register = template.Library()

# steem
from easysteem.easysteem import Oogg

@register.filter(name="upvote")
def upvote(value, arg):# kullanıcı upvote atmış mı atmamışmı
    voters = Oogg(node = None).voters(value.user.username,value.permlink)
    if arg in voters:
        return True
    return False
