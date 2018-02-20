# django
from django.conf.urls import url

#views
from apps.steemitapp.views import convert

urlpatterns = [
    url(r'/sbd-try/', convert.SbdTry.as_view(),name = "steemitapp-convert-sbd-try"),
    url(r'/steem-try/', convert.SteemTry.as_view(),name = "steemitapp-convert-steem-try"),
]
