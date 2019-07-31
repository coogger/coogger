#django
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .utils import paginator

#class
from django.views.generic.base import TemplateView
from django.views import View

#models
from ..models import (UserProfile, Content,  UTopic)
from django_bookmark.models import Bookmark as BookmarkModel

#utils
from .utils import paginator

class Common(TemplateView):
    template_name = "users/user.html"

    def get_context_data(self, username, **kwargs):
        user = User.objects.get(username=username)
        context = super().get_context_data(**kwargs)
        context["current_user"] = user
        context["addresses"] = UserProfile.objects.get(user=user).address.all()
        return context


class UserContent(Common):
    "user's content page"

    def get_context_data(self, username, **kwargs):
        context = super().get_context_data(username, **kwargs)
        user = context["current_user"]
        queryset = Content.objects.filter(user=user, reply=None)
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
        queryset = Content.objects.filter(
            status="ready",
            reply__user=user
        )
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