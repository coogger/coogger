from django.conf.urls import url

# views
from core.cooggerapp.views.home import Home, Search, Report, Review

urlpatterns = [
    url(r'^$', Home.as_view(), name="home"),
    url(r'^search/$', Search.as_view(), name="search"),
    url(r'^report/$', Report.as_view(), name="report"),
    url(r'^review/$', Review.as_view(), name="review"),
    ]
