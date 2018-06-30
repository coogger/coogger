from django.conf.urls import url

#views
from cooggerapp.views import home

urlpatterns = [
    url(r'^$', home.Home.as_view(),name = "home"),
    url(r'^web/search/$',home.Search.as_view(),name = "search"),
    url(r'^web/report/$',home.Report.as_view(),name = "report"),
    url(r"^web/feed/$",home.Feed.as_view(),name="followingcontent"),
    url(r'^web/review/$',home.Review.as_view(),name = "review"),
    url(r'^web/upvote/$',home.Upvote.as_view(),name = "upvote"),
    ]
