from django.urls import path

from ..views.user import About, BadgeView, Bookmark, Comment, UserContent
from ..views.utopic import UserTopic

urlpatterns = [
    path("u/@<username>/about/", About.as_view(), name="userabout"),
    path("@<username>/", UserTopic.as_view(), name="user"),
    path("u/@<username>/comment/", Comment.as_view(), name="comment"),
    path("u/@<username>/bookmark/", Bookmark.as_view(), name="bookmark"),
    path("u/@<username>/content/", UserContent.as_view(), name="usercontent"),
    path("badge/<permlink>/", BadgeView.as_view(), name="badge"),
]
