from rest_framework.serializers import ModelSerializer

# models
from core.cooggerapp.models import (
    Content, OtherInformationOfUsers,
    SearchedWords, OtherAddressesOfUsers,
    Contentviews, Topic)
from core.steemconnect_auth.models import SteemConnectUser, Dapp


class TopicSerializer(ModelSerializer):

    class Meta:
        model = Topic
        fields = ("name", "image_address", "definition", "tags", "address", "editable")


class ContentviewsSerializer(ModelSerializer):

    class Meta:
        model = Contentviews
        fields = ("content", "ip")


class SearchedWordsSerializer(ModelSerializer):

    class Meta:
        model = SearchedWords
        fields = ("word", "hmany")


class OtherAddressesOfUsersSerializer(ModelSerializer):

    class Meta:
        model = OtherAddressesOfUsers
        fields = ("username", "choices", "address")


class DappSerializer(ModelSerializer):

    class Meta:
        model = Dapp
        fields = ("name", "host_name", "redirect_url",
                  "client_id", "app_secret", "login_redirect",
                  "scope", "icon_address", "ms", "management_user",
                   "active", "definition", "image", "active", "beneficiaries")


class SteemConnectUserSerializer(ModelSerializer):

    class Meta:
        model = SteemConnectUser
        fields = (
            "username",
            "dapp_name",
            "dapp",
            "access_token",
            "refresh_token",
            "code",
            )


class UserSerializer(ModelSerializer):

    class Meta:
        model = OtherInformationOfUsers
        fields = (
            "username",
            "about",
            "cooggerup_confirmation",
            "cooggerup_percent",
            "vote_percent",
            "beneficiaries",
            "sponsor",
            "total_votes",
            "total_vote_value",
            "access_token",
            )


class ContentsSerializer(ModelSerializer):
    class Meta:
        model = Content
        fields = (
            "id",
            "dapp_name",
            'username',
            'title',
            'permlink',
            'content',
            "tags",
            "definition",
            "category",
            "language",
            "topic",
            "status",
            "views",
            "mod",
            "modusername",
            "cooggerup",
            "address",
            "created",
            "last_update",
            )
