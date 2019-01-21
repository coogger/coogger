# rest
from rest_framework.viewsets import ModelViewSet

# permissions
from rest.permissions import ApiPermission

# django
from django.core.exceptions import FieldError
from django.contrib.auth.models import User

# api serializers
from rest.serializers import (
    UserSerializer, ContentsSerializer, SteemConnectUserSerializer,
    SearchedWordsSerializer, OtherAddressesOfUsersSerializer, DappSerializer)

# models
from cooggerapp.models import (Content,
    OtherInformationOfUsers, SearchedWords,
    OtherAddressesOfUsers)
from steemconnect_auth.models import Dapp, SteemConnectUser


class Filter(ModelViewSet):
    model = OtherInformationOfUsers
    queryset = model.objects.all()
    serializer_class = []
    permission_classes = [ApiPermission]

    def get_queryset(self):
        items = self.request.GET.items()
        for attr, value in items:
            if attr == "username":
                value = User.objects.filter(username=value)[0]
                attr = "user"
            elif attr == "dapp":
                value = Dapp.objects.filter(name=value)[0]
            if attr == "tags":
                try:
                    self.queryset = self.queryset.filter(tags__contains = value)
                except FieldError:
                    pass
            else:
                try:
                    self.queryset = self.queryset.filter(**{attr: value})
                except FieldError:
                    pass
        return self.queryset

class UserFilter(Filter):
    model = OtherInformationOfUsers
    # queryset = model.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [ApiPermission]


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


class DappFilter(Filter):
    model = Dapp
    queryset = model.objects.all()
    serializer_class = DappSerializer
