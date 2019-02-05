# rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response

# permissions
from core.api.permissions import ApiPermission

# django
from django.http import Http404
from django.contrib.auth.models import User
from django.core.exceptions import FieldError

# api serializers
from core.api.serializers import (
    UserSerializer, ContentsSerializer, SteemConnectUserSerializer)

# models
from core.cooggerapp.models import (Content, OtherInformationOfUsers)
from steemconnect_auth.models import SteemConnectUser


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
        # set_new_access_token function in core.steemconnect_auth lib from models.py is
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
