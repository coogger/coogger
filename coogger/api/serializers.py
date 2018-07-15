from rest_framework import serializers

# models
from cooggerapp.models import Content,OtherInformationOfUsers
from django_steemconnect.models import SteemConnectUser

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

class SuperUserSerializer(serializers.ModelSerializer): # permission

    class Meta:
        model = SteemConnectUser
        fields = (
            'username',
            "access_token",
            "refresh_token",
            "code",
            "community_name",
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
