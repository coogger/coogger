from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView

from ...models import UserProfile
from ..utils import get_current_user


class UserMixin(ListView):
    template_name = "users/user.html"
    paginate_by = 10
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.user = self.get_user()
        context.update(
            current_user=get_current_user(self.user),
            addresses=UserProfile.objects.get(user=self.user).address.all(),
        )
        return context

    def get_user(self):
        return get_object_or_404(User, username=self.kwargs.get("username"))

    def render_to_response(self, context, **response_kwargs):
        if not self.user.is_active:
            return redirect(reverse("user", kwargs=dict(username="ghost")))
        return super().render_to_response(context, **response_kwargs)
