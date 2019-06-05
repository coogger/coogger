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

    class Meta:
        model = Content
        fields = [
            "id", "username", "category_name", "utopic_permlink", "avatar_url",
            "get_absolute_url", "views", "upvote_count", "downvote_count", "body", "language",
            "tags", "definition", "status", "mod_username", "reply_count", 
            "title", "created", "utopic_permlink", "permlink"
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
    
    class Meta:
        model = Issue
        fields = ["__all__"]