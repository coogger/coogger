from django.urls import path

from ..views.home import Feed, Home, Report, Search

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("search/", Search.as_view(), name="search"),
    path("report/<content_id>/", Report.as_view(), name="report"),
    path("@<username>/feed/", Feed.as_view(), name="feed"),
]
