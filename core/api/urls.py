from rest_framework import routers

from django.conf.urls import url, include
from core.api.views.filter import (UserFilter, ContentFilter,
SearchedWordsFilter, OtherAddressesOfUsersFilter,
SteemConnectUserFilter, ContentviewsFilter, TopicFilter)
from core.api.views.view_or_update import (SteemConnectUserApi, UserApi,
    ContentApi, DappApi)

router = routers.DefaultRouter()

router.register(r'filter-steemconnect-user', SteemConnectUserFilter)
router.register(r'filter-content-views-filter', ContentviewsFilter)
router.register(r'filter-topic', TopicFilter)
router.register(r'filter-user', UserFilter)
router.register(r'filter-content', ContentFilter)
router.register(r'filter-searched', SearchedWordsFilter)
router.register(r'filter-useraddresses', OtherAddressesOfUsersFilter)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^content/@(?P<username>.*)/(?P<permlink>.*)/$', ContentApi.as_view()),
    url(r'^user/@(?P<username>.*)/$', UserApi.as_view()),
    url(r'^dapp/(?P<client_id>.*)/$', DappApi.as_view()),
    url(r'^steemconnectuser/@(?P<username>.*)/$', SteemConnectUserApi.as_view()),
]
