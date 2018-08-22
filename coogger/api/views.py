# rest
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

# permissions
from api.permissions import ApiPermission

# django
from django.http import Http404
from django.contrib.auth.models import User

# api serializers
from api.serializers import (
    UserSerializer, ContentsSerializer, SteemConnectUserSerializer)

# models
from cooggerapp.models import Content, OtherInformationOfUsers, Community
from django_steemconnect.models import SteemConnectUser


class SteemConnectUserApi(APIView):
    model = SteemConnectUser
    serialize = SteemConnectUserSerializer
    permission_classes = [ApiPermission]

    def get(self, request, username):
        user = self.model.objects.get(user=self.get_user(username))
        serialized_user = self.serialize(user)
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

    def post(self, request, username, permlink):
        obj = self.model.objects.get(user=self.get_user(username), permlink=permlink)
        for attr, value in request.POST.items():
            setattr(obj, attr, value)
        obj.save()
        return self.get(request, username, permlink)


class UserFilter(ModelViewSet):
    model = OtherInformationOfUsers
    queryset = model.objects.all()
    serializer_class = UserSerializer
    permission_classes = [ApiPermission]

    def get_queryset(self):
        for attr, value in self.request.GET.items():
            self.queryset = self.queryset.filter(**{attr: value})
        return self.queryset


class ContentFilter(ModelViewSet):
    model = Content
    queryset = model.objects.all()
    serializer_class = ContentsSerializer
    permission_classes = [ApiPermission]

    def get_queryset(self):
        for attr, value in self.request.GET.items():
            self.queryset = self.queryset.filter(**{attr: value})
        return self.queryset
