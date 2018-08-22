from rest_framework import serializers

from rest_framework import serializers

# models
from cooggerapp.models import Content, OtherInformationOfUsers
from django_steemconnect.models import SteemConnectUser


class SteemConnectUserSerializer(serializers.ModelSerializer):  # permission

    class Meta:
        model = SteemConnectUser
        fields = (
            'username',
            "access_token",
            "refresh_token",
            "code",
            "community",
            )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = OtherInformationOfUsers
        fields = (
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
            "community_name",
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
            "modusername",
            "cooggerup",
            )
