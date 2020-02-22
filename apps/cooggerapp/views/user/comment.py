from ....threaded_comment.models import ThreadedComments
from .user import UserMixin


class Comment(UserMixin):
    "user's comment page"
    template_name = "users/history/comment.html"
    extra_context = dict(tab="comment", user_comment=True)

    def get_queryset(self):
        user = self.get_user()
        return ThreadedComments.objects.filter(to=user).exclude(user=user)
