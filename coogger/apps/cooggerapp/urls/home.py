from django.conf.urls import url

#views
from apps.cooggerapp.views import home

urlpatterns = [
    url(r'^$', home.Home.as_view(),name = "cooggerapp-home"),
    url(r'^web/search/$',home.Search.as_view(),name = "cooggerapp-search"),
    url(r'^web/report/$',home.Report.as_view(),name = "cooggerapp-report"),
    url(r"^web/following/content/$",home.Feed.as_view(),name="cooggerapp-followingcontent"),
    url(r'^web/preview/$',home.Review.as_view(),name = "cooggerapp-review"),
    ]
