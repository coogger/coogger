from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ...models import UTopic
from ..utils import get_current_user, paginator


class Contributor(TemplateView):
    template_name = "users/topic/detail/contributors.html"

    def get_context_data(self, username, topic_permlink, **kwargs):
        utopic = UTopic.objects.get(user__username=username, permlink=topic_permlink)
        queryset = utopic.contributors.all()
        context = super().get_context_data(**kwargs)
        context["current_user"] = get_current_user(
            get_object_or_404(User, username=username)
        )
        context["queryset"] = paginator(self.request, queryset)
        context["utopic"] = utopic
        return context
