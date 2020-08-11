from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from ...models import UserProfile
from ..utils import get_current_user


class About(TemplateView):
    template_name = "users/about.html"
    http_method_names = ["get"]
    extra_context = dict(tab="about")

    def get_context_data(self, **kwargs):
        self.user = get_object_or_404(
            User, username=self.kwargs.get("username")
        )
        context = super().get_context_data(**kwargs)
        context["current_user"] = get_current_user(self.user)
        context["addresses"] = UserProfile.objects.get(
            user=self.user
        ).address.all()
        queryset = UserProfile.objects.filter(user=self.user)
        if queryset.exists():
            context["about"] = queryset[0].about
        return context

    def render_to_response(self, context, **response_kwargs):
        if not self.user.is_active:
            return redirect(reverse("user", kwargs=dict(username="ghost")))
        return super().render_to_response(context, **response_kwargs)
