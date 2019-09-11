from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import TemplateView
from django_bookmark.models import Bookmark as BookmarkModel

from ....threaded_comment.models import ThreadedComments
from ...forms import UsernameForm
from ...models import Commit, Content, Issue, UserProfile, UTopic
from ..utils import get_current_user, paginator


class Common(TemplateView):
    template_name = "users/user.html"

    def get_context_data(self, username, **kwargs):
        self.user = get_object_or_404(User, username=username)
        context = super().get_context_data(**kwargs)
        context["current_user"] = get_current_user(self.user)
        context["addresses"] = UserProfile.objects.get(user=self.user).address.all()
        return context

    def render_to_response(self, context, **response_kwargs):
        if not self.user.is_active:
            return redirect(reverse("user", kwargs=dict(username="ghost")))
        return super().render_to_response(context, **response_kwargs)


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
        queryset = BookmarkModel.objects.filter(user=user).order_by("-id")
        context["queryset"] = paginator(self.request, queryset)
        return context


class DeleteAccount(LoginRequiredMixin, TemplateView):
    http_method_names = ["post", "get"]
    template_name = "delete-account.html"
    form_class = UsernameForm

    def get_context_data(self):
        return dict(form=self.form_class())

    def post(self, request):
        user = get_object_or_404(
            User, username=request.POST.get("username"), is_active=True
        )
        if user == request.user:
            ghost_user = User.objects.get(username="ghost")
            # del ops
            UTopic.objects.filter(user=user).delete()
            ThreadedComments.objects.filter(user=user).delete()
            Issue.objects.filter(user=user).update(user=ghost_user)
            Commit.objects.filter(user=user).update(user=ghost_user)
            user.is_active = False
            user.save()
            messages.success(
                request,
                "Your information has been deleted and your account has been permanently flagged",
            )
            return redirect("/")
        messages.warning(request, "Your username does not match.")
        return render(
            request, self.template_name, dict(form=self.form_class(data=request.POST))
        )
