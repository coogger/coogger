from django.contrib.auth.models import User, Group
from rest_framework.serializers import HyperlinkedModelSerializer

# models
from cooggerapp.models import Content

class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class ContentsSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Content
        fields = (
            'username',
            'content_list',
            'permlink',
            'title',
            "definition",
            "content",
            "status",
            "tag",
            "time",
            "dor",
            "views",
            "read",
            "lastmod",
            "modusername",
            "modcomment",
            "approved",
            "cantapproved",
            "cooggerup",
            "upvote",
            )
