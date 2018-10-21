# rest
from rest_framework.viewsets import ModelViewSet

# permissions
from cooggerapi.permissions import ApiPermission

# django
from django.core.exceptions import FieldError

# api serializers
from cooggerapi.serializers import (
    UserSerializer, ContentsSerializer, SteemConnectUserSerializer,
    SearchedWordsSerializer, OtherAddressesOfUsersSerializer, CommunitySerializer)

# models
from cooggerapp.models import (Content,
    OtherInformationOfUsers, SearchedWords,
    OtherAddressesOfUsers)
from steemconnect_auth.models import Community, SteemConnectUser


class UserFilter(ModelViewSet):
    model = OtherInformationOfUsers
    queryset = model.objects.all()
    serializer_class = UserSerializer
    permission_classes = [ApiPermission]

    def get_queryset(self):
        items = self.request.GET.items()
        for attr, value in items:
            try:
                self.queryset = self.queryset.filter(**{attr: value})
            except FieldError:
                pass
        return self.queryset


class SteemConnectUserFilter(UserFilter):
    model = SteemConnectUser
    queryset = model.objects.all()
    serializer_class = SteemConnectUserSerializer

class ContentFilter(UserFilter):
    model = Content
    queryset = model.objects.all()
    serializer_class = ContentsSerializer


class SearchedWordsFilter(UserFilter):
    model = SearchedWords
    queryset = model.objects.all()
    serializer_class = SearchedWordsSerializer


class OtherAddressesOfUsersFilter(UserFilter):
    model = OtherAddressesOfUsers
    queryset = model.objects.all()
    serializer_class = OtherAddressesOfUsersSerializer


class CommunityFilter(UserFilter):
    model = Community
    queryset = model.objects.all()
    serializer_class = CommunitySerializer
