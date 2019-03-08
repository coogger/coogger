from rest_framework.serializers import (
    ModelSerializer)

# models
from core.cooggerapp.models import (
    Content, OtherInformationOfUsers)

from django.contrib.auth.models import User


class ContentSerializer(ModelSerializer):

    class Meta:
        model = Content
        fields = (
            "id", 'username',
            'title', 'permlink',
            'body', "tags",
            "definition", "category_name",
            "language", "topic_name",
            "status", "views",
            "mod", "modusername",
            "cooggerup", "created",
            "last_update", "get_report",
            "get_views", "get_commits")


class UserSerializer(ModelSerializer):

    class Meta:
        model = OtherInformationOfUsers
        fields = (
            "username", "get_user", "get_user_address", "get_steemconnect", "about",
            "cooggerup_confirmation", "sponsor",
            "cooggerup_percent", "vote_percent",
            "beneficiaries", "total_votes",
            "total_vote_value", "access_token",
            )
