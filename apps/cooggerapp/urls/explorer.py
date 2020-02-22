from django.urls import path

from ..views.explorer import Filter, Hashtag, Languages, TopicView
from ..views.home.index import Index

urlpatterns = [
    path("explorer/posts/", Index.as_view(), name="explorer_posts"),
    path("topic/<permlink>/", TopicView.as_view(), name="topic"),
    path("tags/<hashtag>/", Hashtag.as_view(), name="hashtag"),
    path("language/<language>/", Languages.as_view(), name="language"),
    path("filter/", Filter.as_view(), name="filter"),
]
