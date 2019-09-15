from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ...models import UserProfile
from ..utils import get_current_user


class About(TemplateView):
    template_name = "users/about.html"
    http_method_names = ["get"]
    extra_context = dict(tab="about")

    def get_context_data(self, username, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = get_object_or_404(User, username=username)
        context["current_user"] = get_current_user(user)
        context["addresses"] = UserProfile.objects.get(user=user).address.all()
        queryset = UserProfile.objects.filter(user=user)
        if queryset.exists():
            context["about"] = queryset[0].about
        return context
