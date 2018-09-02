from rest_framework import routers

from django.conf.urls import url, include
from cooggerapi.views.filter import (UserFilter, ContentFilter,
SearchedWordsFilter, UserFollowFilter, CommunityFilter,
SteemConnectUserFilter)
from cooggerapi.views.view_or_update import (SteemConnectUserApi, UserApi,
    ContentApi, CommunityApi)

router = routers.DefaultRouter()

router.register(r'filter-steemconnect-user', SteemConnectUserFilter)
router.register(r'filter-user', UserFilter)
router.register(r'filter-content', ContentFilter)
router.register(r'filter-searched', SearchedWordsFilter)
router.register(r'filter-useraddresses', UserFollowFilter)
router.register(r'filter-community', CommunityFilter)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^content/@(?P<username>.*)/(?P<permlink>.*)/$', ContentApi.as_view()),
    url(r'^user/@(?P<username>.*)/$', UserApi.as_view()),
    url(r'^community/(?P<client_id>.*)/$', CommunityApi.as_view()),
    url(r'^steemconnectuser/@(?P<username>.*)/$', SteemConnectUserApi.as_view()),
]
