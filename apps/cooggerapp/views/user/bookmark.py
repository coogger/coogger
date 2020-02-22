from apps.bookmark.models import Bookmark as BookmarkModel

from .user import UserMixin


class Bookmark(UserMixin):
    template_name = "users/bookmark/index.html"
    extra_context = dict(tab="bookmark")

    def get_queryset(self):
        return BookmarkModel.objects.filter(user=self.get_user()).order_by("-id")
