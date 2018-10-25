from django.conf.urls import url

# views
from cooggerapp.views import home

urlpatterns = [
    url(r'^$', home.Home.as_view(), name="home"),
    url(r'^search/$', home.Search.as_view(), name="search"),
    url(r'^report/$', home.Report.as_view(), name="report"),
    url(r"^feed/$", home.Feed.as_view(), name="followingcontent"),
    url(r'^review/$', home.Review.as_view(), name="review"),
    url(r'^dapps/$', home.Dapps.as_view(), name="dapps"),
    url(r'^supporters/$', home.Supporters.as_view(), name="supporters"),
    ]
