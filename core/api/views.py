# rest_framework
from django.contrib.auth.models import User
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

# api serializers
from core.api.serializers import (
    ContentSerializer,
    ContentSerializerToLoad,
    UserSerializer)

# models
from core.cooggerapp.models import (
    Content, OtherInformationOfUsers)

# views
from core.cooggerapp.utils import model_filter


class ListContent(ListCreateAPIView):
    queryset = Content.objects.all()
    permission_classes = []

    def get_object(self):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def filter_queryset(self, queryset):
        return model_filter(
            self.request.query_params.items(),
            self.queryset).get("queryset")

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return ContentSerializer
        return ContentSerializerToLoad


class ListContentToLoad(ListContent):
    queryset = Content.objects.all()
    permission_classes = []

    def get_serializer_class(self):
        return ContentSerializerToLoad


class ListUser(ListContent):
    queryset = OtherInformationOfUsers.objects.all()
    serializer_class = UserSerializer
