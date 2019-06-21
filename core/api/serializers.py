from rest_framework import serializers

# models
from core.cooggerapp.models import (
    Content,
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
    mod_username = serializers.ReadOnlyField(
        source="mod.username"
    )
    parent_user = serializers.ReadOnlyField(
        source="get_parent.username"
    )
    parent_id = serializers.ReadOnlyField(
        source="get_parent.id"
    )

    class Meta:
        model = Content
        fields = [
            "id", "username", "category_name", "utopic_permlink", "avatar_url",
            "get_absolute_url", "views", "upvote_count", "downvote_count", "body", "language",
            "tags", "definition", "status", "mod_username", "reply_count", 
            "title", "created", "utopic_permlink", "permlink", "get_absolute_url", 
            "parent_permlink", "parent_user", "parent_id"
        ]


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
    parent_user = serializers.ReadOnlyField(
        source="get_parent.username"
    )
    parent_id = serializers.ReadOnlyField(
        source="get_parent.id"
    )

    class Meta:
        model = Issue
        fields = [
            "id", "username", "permlink",
            "utopic_permlink", "avatar_url", "body",
            "status", "issue_id",
            "title", "reply", "reply_count",
            "created", "last_update",
            "parent_user", "parent_permlink", "get_absolute_url",
            "views", "upvote_count", "downvote_count", "parent_id",
        ]