from django.conf.urls import url

#views
from apps.steemitapp.views import home

urlpatterns = [
    url(r'^$', home.Home.as_view(),name = "steemitapp-home"),
    url(r'^search/$', home.Search.as_view(),name = "steemitapp-search"),
]
