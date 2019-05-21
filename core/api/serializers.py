from rest_framework.serializers import (
    ModelSerializer)

# models
from core.cooggerapp.models import (
    Content,
    OtherInformationOfUsers,
    Commit,
    Issue
    )

from django.contrib.auth.models import User


class ContentSerializer(ModelSerializer):

    class Meta:
        model = Content
        fields = (
            "id", 'username',
            'title', 'permlink',
            "definition", "category_name",
            "language", "topic_name",
            "views")


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


class CommitSerializer(ModelSerializer):

    class Meta:
        model = Commit
        fields = [
            "content_absolute_url",
            "hash",
            "username",
            "topic_name",
            "body",
            "msg",
            "created",
        ]


class IssueSerializer(ModelSerializer):
    
    class Meta:
        model = Issue
        fields = [
            "id",
            "username",
            "topic_permlink",
            "permlink",
            "parent_username",
            "parent_permlink",
            "title",
            "body",
            "reply",
            "status",
            "reply_count",
            "created",
        ]