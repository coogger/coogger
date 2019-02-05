# rest_framework
from rest_framework.viewsets import ModelViewSet

# permissions
from core.api.permissions import ApiPermission

# django
from django.contrib.auth.models import User

# api serializers
from core.api.serializers import (
    UserSerializer, ContentsSerializer, SteemConnectUserSerializer,
    SearchedWordsSerializer, OtherAddressesOfUsersSerializer, DappSerializer,
    ContentviewsSerializer, TopicSerializer)

# models
from core.cooggerapp.models import (Content,
    OtherInformationOfUsers, SearchedWords,
    OtherAddressesOfUsers, Contentviews, Topic)
from core.steemconnect_auth.models import SteemConnectUser

# views
from core.cooggerapp.utils import content_by_filter

class Filter(ModelViewSet):
    model = OtherInformationOfUsers
    queryset = model.objects.all()
    serializer_class = []
    permission_classes = [ApiPermission]

    def get_queryset(self):
        return content_by_filter(
            self.request.GET.items(), self.queryset
            ).get("queryset")

class UserFilter(Filter):
    model = OtherInformationOfUsers
    serializer_class = UserSerializer


class ContentviewsFilter(Filter):
    model = Contentviews
    queryset = model.objects.all()
    serializer_class = ContentviewsSerializer


class TopicFilter(Filter):
    model = Topic
    queryset = model.objects.all()
    serializer_class = TopicSerializer


class SteemConnectUserFilter(Filter):
    model = SteemConnectUser
    queryset = model.objects.all()
    serializer_class = SteemConnectUserSerializer


class ContentFilter(Filter):
    model = Content
    queryset = model.objects.all()
    serializer_class = ContentsSerializer
    permission_classes = []


class SearchedWordsFilter(Filter):
    model = SearchedWords
    queryset = model.objects.all()
    serializer_class = SearchedWordsSerializer
    permission_classes = []


class OtherAddressesOfUsersFilter(Filter):
    model = OtherAddressesOfUsers
    queryset = model.objects.all()
    serializer_class = OtherAddressesOfUsersSerializer
    permission_classes = []
