from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django_bookmark.models import Bookmark as BookmarkModel

from ...threaded_comment.models import ThreadedComments
from ..models import Content, UserProfile
from .utils import paginator


class Common(TemplateView):
    template_name = "users/user.html"

    def get_context_data(self, username, **kwargs):
        user = get_object_or_404(User, username=username)
        context = super().get_context_data(**kwargs)
        context["current_user"] = user
        context["addresses"] = UserProfile.objects.get(user=user).address.all()
        return context


class UserContent(Common):
    "user's content page"

    def get_context_data(self, username, **kwargs):
        context = super().get_context_data(username, **kwargs)
        user = context["current_user"]
        queryset = Content.objects.filter(user=user)
        if user != self.request.user:
            queryset = queryset.filter(status="ready")
        context["queryset"] = paginator(self.request, queryset)
        return context


class About(Common):
    template_name = "users/about.html"

    def get_context_data(self, username, *args, **kwargs):
        context = super().get_context_data(username, **kwargs)
        user = context["current_user"]
        queryset = UserProfile.objects.filter(user=user)
        if queryset.exists():
            context["about"] = queryset[0].about
        return context


class Comment(Common):
    "user's comment page"
    template_name = "users/history/comment.html"

    def get_context_data(self, username, **kwargs):
        context = super().get_context_data(username, **kwargs)
        user = context["current_user"]
        queryset = ThreadedComments.objects.filter(to=user).exclude(user=user)
        context["user_comment"] = True
        context["queryset"] = paginator(self.request, queryset)
        return context


class Bookmark(Common):
    template_name = "users/bookmark/index.html"

    def get_context_data(self, username, **kwargs):
        context = super().get_context_data(username, **kwargs)
        user = context["current_user"]
        queryset = BookmarkModel.objects.filter(user=user)
        context["queryset"] = paginator(self.request, queryset)
        return context
