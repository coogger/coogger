from django.conf.urls import url

#views
from cooggerapp.views import home

urlpatterns = [
    url(r'^$', home.Home.as_view(),name = "home"),
    url(r'^search/$',home.Search.as_view(),name = "search"),
    url(r'^report/$',home.Report.as_view(),name = "report"),
    url(r"^feed/$",home.Feed.as_view(),name="followingcontent"),
    url(r'^review/$',home.Review.as_view(),name = "review"),
    url(r'^upvote/$',home.Upvote.as_view(),name = "upvote"),
    url(r'^communities/$',home.Communities.as_view(),name = "communities"),
    ]
