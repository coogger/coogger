from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

# api serializers
from api.serializers import UserSerializer, ContentsSerializer,SuperUserSerializer

# models
from cooggerapp.models import Content,OtherInformationOfUsers
from django.contrib.auth.models import User

class UserViewSet(ModelViewSet):
    queryset = OtherInformationOfUsers.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        if "username" in self.request.GET:
            get_user = User.objects.filter(username = self.request.GET["username"])[0]
            self.queryset = self.queryset.filter(user = get_user)
        if self.request.user.is_superuser:
            self.serializer_class = SuperUserSerializer
        return self.queryset

class ContentsViewSet(ModelViewSet):
    queryset = Content.objects.filter(status = "approved").order_by("-time")
    serializer_class = ContentsSerializer

    def get_queryset(self):
        if "username" in self.request.GET:
            get_user = User.objects.filter(username = self.request.GET["username"])[0]
            self.queryset = self.queryset.filter(user = get_user)
        if "permlink" in self.request.GET:
            self.queryset = self.queryset.filter(permlink = self.request.GET["permlink"])
        return self.queryset
