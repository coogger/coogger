from rest_framework import serializers

# models
from cooggerapp.models import Content, OtherInformationOfUsers, SearchedWords, UserFollow
from django_steemconnect.models import SteemConnectUser, Community


class SearchedWordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SearchedWords
        fields = ("word", "hmany")


class UserFollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFollow
        fields = ("username", "choices", "adress")


class CommunitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Community
        fields = ("name", "host_name", "redirect_url",
                  "client_id", "app_secret", "login_redirect",
                  "scope", "icon_address", "ms", "management_user", "management")


class SteemConnectUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = SteemConnectUser
        fields = (
            'user',
            "username",
            "access_token",
            "refresh_token",
            "code",
            "community",
            "community_name"
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
            )


class ContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = (
            "community",
            "community_name",
            "user",
            'username',
            'title',
            'permlink',
            'content',
            "tag",
            "category",
            "language",
            "definition",
            "topic",
            "status",
            "time",
            "dor",
            "views",
            "read",
            "lastmod",
            "mod",
            "modusername",
            "cooggerup",
            )
