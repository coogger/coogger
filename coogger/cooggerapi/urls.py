from rest_framework import routers

from django.conf.urls import url, include
from cooggerapi.views import SteemConnectUserApi, UserApi, ContentApi, UserFilter, ContentFilter

router = routers.DefaultRouter()
router.register(r'filter-user', UserFilter)
router.register(r'filter-content', ContentFilter)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^content/@(?P<username>.*)/(?P<permlink>.*)/$', ContentApi.as_view()),
    url(r'^user/@(?P<username>.*)/$', UserApi.as_view()),
    url(r'^steemconnectuser/@(?P<username>.*)/$', SteemConnectUserApi.as_view()),
]
