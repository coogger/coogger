# rest
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

# permissions
from cooggerapi.permissions import ApiPermission, FilterPermission

# django
from django.http import Http404
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import FieldError

# api serializers
from cooggerapi.serializers import (
    UserSerializer, ContentsSerializer, SteemConnectUserSerializer,
    SearchedWordsSerializer, UserFollowSerializer, CommunitySerializer)

# models
from cooggerapp.models import (Content,
    OtherInformationOfUsers, Community, SearchedWords,
    UserFollow)
from django_steemconnect.models import SteemConnectUser, Community

PAGE_SIZE = settings.REST_FRAMEWORK["PAGE_SIZE"]


class SteemConnectUserApi(APIView):
    model = SteemConnectUser
    serialize = SteemConnectUserSerializer
    permission_classes = [ApiPermission]

    def get(self, request, username):
        queryset = self.model.objects.get(user=self.get_user(username))
        serialized_user = self.serialize(queryset)
        return Response(serialized_user.data)

    def post(self, request, username):
        obj = self.model.objects.get(user=self.get_user(username))
        for attr, value in request.POST.items():
            setattr(obj, attr, value)
        obj.save()
        return self.get(request, username)

    def get_user(self, username):
        try:
            return User.objects.filter(username=username)[0]
        except User.DoesNotExist:
            raise Http404

    def set_new_access_token(self):
        # TODO: new Features! if this function is run,
        # set_new_access_token function in django_steemconnect lib from models.py is
        # run and share coogger and steem blockchain
        pass


class UserApi(SteemConnectUserApi):
    model = OtherInformationOfUsers
    serialize = UserSerializer


class ContentApi(SteemConnectUserApi):
    model = Content
    serialize = ContentsSerializer


    def get(self, request, username, permlink):
        content = self.model.objects.get(user=self.get_user(username), permlink=permlink)
        serialized_user = self.serialize(content)
        return Response(serialized_user.data)

    def post(self, request, username, permlink): # TODO: Features like permalink should not be updated.
        obj = self.model.objects.get(user=self.get_user(username), permlink=permlink)
        for attr, value in request.POST.items():
            setattr(obj, attr, value)
        obj.save()
        return self.get(request, username, permlink)

    def share(self):
        # TODO: new Features! if this function is run,
        # content_save function from models.py is run and share coogger and steem blockchain
        pass


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
