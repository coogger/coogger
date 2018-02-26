# django
from django.conf.urls import url

#views
from apps.steemitapp.views.convert import Koinim,Binance

urlpatterns = [
    url(r'/koinim-sbd-try/', Koinim.as_view(),name = "steemitapp-convert-koinim-sbd-try"),
    url(r'/koinim-steem-try/', Koinim.as_view(),name = "steemitapp-convert-koinim-steem-try"),
    url(r'/koinim-btc-try/', Koinim.as_view(),name = "steemitapp-convert-koinim-btc-try"),

    url(r'/binance-steem-try/', Binance.as_view(),name = "steemitapp-convert-binance-steem-try"),
    url(r'/binance-sbd-try/', Binance.as_view(),name = "steemitapp-convert-binance-sbd-try"),

]
