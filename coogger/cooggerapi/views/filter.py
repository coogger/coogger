# rest
from rest_framework.viewsets import ModelViewSet

# permissions
from cooggerapi.permissions import FilterPermission

# django
from django.core.exceptions import FieldError

# api serializers
from cooggerapi.serializers import (
    UserSerializer, ContentsSerializer, SteemConnectUserSerializer,
    SearchedWordsSerializer, UserFollowSerializer, CommunitySerializer)

# models
from cooggerapp.models import (Content,
    OtherInformationOfUsers, SearchedWords,
    UserFollow)
from django_steemconnect.models import Community, SteemConnectUser


class UserFilter(ModelViewSet):
    model = OtherInformationOfUsers
    queryset = model.objects.all()
    serializer_class = UserSerializer
    permission_classes = [FilterPermission]

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


class UserFollowFilter(UserFilter):
    model = UserFollow
    queryset = model.objects.all()
    serializer_class = UserFollowSerializer


class CommunityFilter(UserFilter):
    model = Community
    queryset = model.objects.all()
    serializer_class = CommunitySerializer
