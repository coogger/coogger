from django.urls import path

from .views import Follow, GetFollower

urlpatterns = [
    path("@<username>/", Follow.as_view(), name="follow"),
    path("get/", GetFollower.as_view(), name="get_followers"),
]
