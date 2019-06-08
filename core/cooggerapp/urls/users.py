# django
from django.urls import path

# views
from ..views.users import (About, Home, Comment)

urlpatterns = [
    path('u/@<username>/about/', About.as_view(), name="userabout"),
    path('@<username>/', Home.as_view(), name="user"),
    path('u/@<username>/comment/', Comment.as_view(), name="comment"),
    ]
