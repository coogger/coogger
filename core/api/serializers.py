from rest_framework import serializers

# models
from core.cooggerapp.models import (
    Content, OtherInformationOfUsers,
    SearchedWords, OtherAddressesOfUsers,
    Contentviews, Topic)
from core.steemconnect_auth.models import SteemConnectUser, Dapp


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ("name", "image_address", "definition")


class ContentviewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contentviews
        fields = ("content", "ip")


class SearchedWordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SearchedWords
        fields = ("word", "hmany")


class OtherAddressesOfUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = OtherAddressesOfUsers
        fields = ("username", "choices", "address")


class DappSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dapp
        fields = ("name", "host_name", "redirect_url",
                  "client_id", "app_secret", "login_redirect",
                  "scope", "icon_address", "ms", "management_user", "management","active")


class SteemConnectUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = SteemConnectUser
        fields = (
            'user',
            "username",
            "access_token",
            "refresh_token",
            "code",
            "dapp",
            "dapp_name"
            )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = OtherInformationOfUsers
        fields = (
            "user",
            'username',
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


class ContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = (
            "id",
            "created",
            "dapp",
            "dapp_name",
            "user",
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
            )
