from rest_framework import routers

from django.conf.urls import url, include
from core.api.views import (ListContent, ListUser)


urlpatterns = [
    url(r'^content/$', ListContent.as_view()),
    url(r'^user/$', ListUser.as_view()),
]
