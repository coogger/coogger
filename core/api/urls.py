from rest_framework import routers
from django.urls import include, path

from core.api.views import (ListContent, ListUser, ListContentToLoad)


urlpatterns = [
    path('content/', ListContent.as_view()),
    path('content-to-load/', ListContentToLoad.as_view()),
    path('user/', ListUser.as_view()),
]
