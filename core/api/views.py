# rest_framework
# from django.contrib.auth.models import User
from rest_framework.generics import ListCreateAPIView
# from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
# from rest_framework.serializers import ModelSerializer
# from rest_framework.views import APIView

# api serializers
from core.api.serializers import (
    ContentSerializer,
    UserSerializer,
    CommitSerializer,
    IssueSerializer,
    )

# models
from core.cooggerapp.models import (
    Content,
    OtherInformationOfUsers,
    Commit,
    Issue,
    )

# views
from core.cooggerapp.views.utils import model_filter


class ListContent(ListCreateAPIView):
    model = Content
    serializer_class = ContentSerializer
    permission_classes = []

    def get_object(self):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def filter_queryset(self, queryset):
        return model_filter(
            self.request.query_params.items(),
            self.get_queryset()).get("queryset")

    def get_queryset(self):
        return self.model.objects.all()


class ListUser(ListContent):
    model = OtherInformationOfUsers
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.model.objects.filter(user=self.request.user)
        return None


class ListCommit(ListContent):
    model = Commit
    serializer_class = CommitSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.model.objects.filter(user=self.request.user)
        return None


class ListIssue(ListContent):
    model = Issue
    serializer_class = IssueSerializer