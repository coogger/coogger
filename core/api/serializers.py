from rest_framework import serializers

# models
from core.cooggerapp.models import (
    Content,
    OtherInformationOfUsers,
    Commit,
    Issue
    )

from django.contrib.auth.models import User


class ContentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(
        source="user.username"
    )
    category_name = serializers.ReadOnlyField(
        source="category.name"
    )
    utopic_permlink = serializers.ReadOnlyField(
        source="utopic.permlink"
    )
    avatar_url = serializers.ReadOnlyField(
        source="user.githubauthuser.avatar_url"
    )

    class Meta:
        model = Content
        fields = ("__all__")
        read_only_fields = ("__all__", )


class UserSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(
        source="user.username"
    )
    first_name = serializers.ReadOnlyField(
        source="user.first_name"
    )
    last_name = serializers.ReadOnlyField(
        source="user.last_name"
    )
    id = serializers.ReadOnlyField(
        source="user.id"
    )


    class Meta:
        model = OtherInformationOfUsers
        fields = (
            "username",
            "first_name",
            "last_name",
            "id",
            )
        read_only_fields = ("__all__", )


class CommitSerializer(serializers.ModelSerializer):
    content_absolute_url = serializers.ReadOnlyField(
        source="content.get_absolute_url"
    )
    username = serializers.ReadOnlyField(
        source="user.username"
    )
    topic_name = serializers.ReadOnlyField(
        source="utopic.name"
    )

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
        read_only_fields = ("__all__", )


class IssueSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(
        source="user.username"
    )
    utopic_permlink = serializers.ReadOnlyField(
        source="utopic.permlink"
    )
    avatar_url = serializers.ReadOnlyField(
        source="user.githubauthuser.avatar_url"
    )
    
    class Meta:
        model = Issue
        fields = [
            "id",
            "username",
            "permlink",
            "utopic_permlink",
            "avatar_url",
            "parent_username",
            "parent_permlink",
            "title",
            "body",
            "reply",
            "status",
            "reply_count",
            "created",
        ]
        read_only_fields = ("__all__", )