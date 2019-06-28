# django
from django.urls import path

# views
from ..views.users import (About, Comment, Bookmark, UserContent)
from ..views.utopic import (UserTopic)

urlpatterns = [
    path('u/@<username>/about/', About.as_view(), name="userabout"),
    path('@<username>/', UserTopic.as_view(), name="user"),
    path('u/@<username>/comment/', Comment.as_view(), name="comment"),
    path('u/@<username>/bookmark/', Bookmark.as_view(), name="bookmark"),
    path('u/@<username>/content/', UserContent.as_view(), name="usercontent"),
    ]
