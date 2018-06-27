from rest_framework import serializers

# models
from cooggerapp.models import Content,OtherInformationOfUsers

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = OtherInformationOfUsers
        fields = (
            'username',
            "about",
            "hmanycontent",
            "cooggerup_confirmation",
            "cooggerup_percent",
            "vote_percent",
            "beneficiaries",
            )

class SuperUserSerializer(serializers.ModelSerializer): # permission

    class Meta:
        model = OtherInformationOfUsers
        fields = (
            'username',
            "about",
            "hmanycontent",
            "cooggerup_confirmation",
            "cooggerup_percent",
            "vote_percent",
            "beneficiaries",
            "get_access_token",
            )

class ContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = (
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
            )
