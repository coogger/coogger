from django.urls import path

from ..views.home import Feed, Index, Report, Search

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("search/", Search.as_view(), name="search"),
    path("report/<content_id>/", Report.as_view(), name="report"),
    path("@<username>/feed/", Feed.as_view(), name="feed"),
]
