from ...models import Content
from .user import UserMixin


class UserContent(UserMixin):
    "user's content page"
    extra_context = dict(tab="content")

    def get_queryset(self):
        user = self.get_user()
        queryset = Content.objects.filter(user=user)
        if user != self.request.user:
            return queryset.filter(status="ready")
        return queryset
