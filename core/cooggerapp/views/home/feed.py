from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse

from ...models import Content
from .index import Index


class Feed(Index):
    # TODO this class must be improved
    # make a new model for this op
    template_name = "card/blogs.html"

    def get_queryset(self):
        following = list(
            get_object_or_404(User, username=self.username).follow.following.all()
        )
        queryset = Content.objects.filter(user__in=following, status="ready")
        return queryset
