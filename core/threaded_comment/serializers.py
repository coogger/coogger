from rest_framework import serializers

from .models import ThreadedComments


class ReplySerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    avatar_url = serializers.ReadOnlyField(source="user.githubauthuser.avatar_url")
    parent_user = serializers.ReadOnlyField(source="get_parent.username")
    parent_id = serializers.ReadOnlyField(source="get_parent.id")
    reply_count = serializers.ReadOnlyField()
    permlink = serializers.ReadOnlyField()
    image_address = serializers.ReadOnlyField()

    class Meta:
        model = ThreadedComments
        fields = [
            "id",
            "app_label",
            "model_name",
            "content_type",
            "object_id",
            "username",
            "reply",
            "avatar_url",
            "body",
            "image_address",
            "permlink",
            "reply_count",
            "depth",
            "get_absolute_url",
            "views",
            "upvote_count",
            "downvote_count",
            "parent_permlink",
            "parent_user",
            "parent_id",
            "created",
        ]
