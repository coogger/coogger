from django.contrib.auth.models import User, Group
from rest_framework.viewsets import ModelViewSet
from api.serializers import UserSerializer, ContentsSerializer

from cooggerapp.models import Content

class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class ContentsViewSet(ModelViewSet):
    queryset = Content.objects.filter(status = "approved").order_by("-time")
    serializer_class = ContentsSerializer
