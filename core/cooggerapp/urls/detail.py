# django
from django.conf.urls import url
from django.shortcuts import redirect

# views
from core.cooggerapp.views.detail import Embed, Detail


def detail_redirect(request, steem_category, username, permlink):
    return redirect(f"/@{username}/{permlink}")


urlpatterns = [
    url(r'^embed/@(?P<username>.+)/(?P<permlink>.+)/$', Embed.as_view(), name="embed"),
    url(r'^(?P<steem_category>.+)/@(?P<username>.+)/(?P<permlink>.+)/$', detail_redirect, name="detail_redirect"),
    url(r'^@(?P<username>.+)/(?P<permlink>.+)/$', Detail.as_view(), name="detail"),
    ]
