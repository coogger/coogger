from rest_framework.viewsets import ModelViewSet

# api serializers
from api.serializers import (
    UserSerializer, ContentsSerializer, SuperUserSerializer)

# models
from cooggerapp.models import Content, OtherInformationOfUsers, Community
from django_steemconnect.models import SteemConnectUser
from django.contrib.auth.models import User


class UserViewSet(ModelViewSet):
    queryset = OtherInformationOfUsers.objects.all()
    main_queryset = queryset
    serializer_class = UserSerializer
    main_serializer_class = serializer_class

    def get_queryset(self):
        if self.request.user.is_superuser:
            self.serializer_class = SuperUserSerializer
            self.queryset = SteemConnectUser.objects.all()
            self.username = self.request.GET.get("username", None)
            if self.username is not None:
                self.get_user = User.objects.filter(username=self.username)[0]
                self.queryset = self.queryset.filter(user=self.get_user)
            default = self.request.GET.get("default", None)
            if default is not None:
                return self.default()
            new_access_token = self.request.GET.get("new_access_token", None)
            if bool(new_access_token) == True:
                return self.update_access_token()
        return self.queryset

    def default(self):
        self.queryset = self.main_queryset
        self.serializer_class = self.main_serializer_class
        if self.username is not None:
            self.queryset = self.main_queryset.filter(user=self.get_user)
        cooggerup_confirmation = self.request.GET.get("cooggerup_confirmation", None)
        if cooggerup_confirmation is not None:
            self.queryset = self.main_queryset.filter(cooggerup_confirmation=cooggerup_confirmation)
            return self.queryset

    def update_access_token(self):
        access_token = self.request.GET.get("access_token")
        # refresh_token = self.request.GET.get("refresh_token")
        # code = self.request.GET.get("code")
        model = SteemConnectUser
        model_filter = model.objects.filter(user=self.get_user)
        # refresh_token=refresh_token,code=code
        model_filter.update(access_token=access_token)
        return True


class ContentsViewSet(ModelViewSet):
    queryset = Content.objects.all().order_by("-time")
    serializer_class = ContentsSerializer

    def get_queryset(self):
        username = self.request.GET.get("username", None)
        permlink = self.request.GET.get("permlink", None)
        community_name = self.request.GET.get("community_name", None)
        status = self.request.GET.get("status", None)
        mod = self.request.GET.get("mod", None)
        category = self.request.GET.get("category", None)
        language = self.request.GET.get("language", None)
        topic = self.request.GET.get("topic", None)
        dor = self.request.GET.get("dor", None)
        views = self.request.GET.get("views", None)
        read = self.request.GET.get("read", None)
        cooggerup = self.request.GET.get("cooggerup", None)
        was_voting_done = self.request.GET.get("was_voting_done", None)

        if username is not None:
            get_user = User.objects.filter(username=self.request.GET["username"])[0]
            self.queryset = self.queryset.filter(user=get_user)

        if permlink is not None:
            self.queryset = self.queryset.filter(permlink=self.request.GET["permlink"])

        if was_voting_done is not None:
            Content.objects.filter(user=get_user, permlink=permlink).update(cooggerup=self.request.GET["was_voting_done"])

        if community_name is not None:
            community_name = Community.objects.filter(name=self.request.GET["username"])[0]
            self.queryset = self.queryset.filter(community=community_name, user=get_user)

        if status is not None:
            self.queryset = self.queryset.filter(status=self.request.GET["status"])

        if mod is not None:
            get_mod = User.objects.filter(username=self.request.GET["mod"])[0]
            self.queryset = self.queryset.filter(mod=get_mod)

        if category is not None:
            self.queryset = self.queryset.filter(category=self.request.GET["category"])

        if language is not None:
            self.queryset = self.queryset.filter(language=self.request.GET["language"])

        if topic is not None:
            self.queryset = self.queryset.filter(topic=self.request.GET["topic"])

        if dor is not None:
            self.queryset = self.queryset.filter(dor=self.request.GET["dor"])

        if views is not None:
            self.queryset = self.queryset.filter(views=self.request.GET["views"])

        if read is not None:
            self.queryset = self.queryset.filter(read=self.request.GET["read"])

        if cooggerup is not None:
            self.queryset = self.queryset.filter(cooggerup=self.request.GET["cooggerup"])

        return self.queryset
