# django
from django.urls import path

# views
from core.cooggerapp.views.users import (About, Home, Comment, Activity)

urlpatterns = [
    path('u/@<username>/about/', About.as_view(), name="userabout"),
    path('@<username>/', Home.as_view(), name="user"),
    path('u/@<username>/comment/', Comment.as_view(), name="comment"),
    path('u/@<username>/activity/', Activity.as_view(), name="activity"),
    ]
