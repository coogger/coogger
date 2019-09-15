from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from ...models import UTopic
from ..utils import get_current_user


class Contributor(ListView):
    template_name = "users/topic/detail/contributors.html"
    paginate_by = 10
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            current_user=get_current_user(self.user),
            utopic=self.utopic
        )
        return context

    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs.get("username"))
        self.utopic = UTopic.objects.get(
            user=self.user,
            permlink=self.kwargs.get("topic_permlink")
        )
        return self.utopic.get_contributors
