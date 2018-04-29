# django
from django.conf.urls import include, url
#views
from cooggerup.views.convert import Koinim,Binance
from cooggerup.views import home

urlpatterns = [
    url(r'^$', home.Home.as_view(),name = "cooggerup-home"),
    url(r'^search/$', home.Search.as_view(),name = "cooggerup-search"),
    url(r'/koinim-sbd-try/', Koinim.as_view(),name = "cooggerup-convert-koinim-sbd-try"),
    url(r'/koinim-steem-try/', Koinim.as_view(),name = "cooggerup-convert-koinim-steem-try"),
    url(r'/koinim-btc-try/', Koinim.as_view(),name = "cooggerup-convert-koinim-btc-try"),
    url(r'/binance-steem-try/', Binance.as_view(),name = "cooggerup-convert-binance-steem-try"),
    url(r'/binance-sbd-try/', Binance.as_view(),name = "cooggerup-convert-binance-sbd-try"),
]
