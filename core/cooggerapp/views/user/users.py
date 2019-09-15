from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView, TemplateView
from django_bookmark.models import Bookmark as BookmarkModel

from ....threaded_comment.models import ThreadedComments
from ...forms import UsernameForm
from ...models import Commit, Content, Issue, UserProfile, UTopic
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


class UserContent(UserMixin):
    "user's content page"
    extra_context = dict(tab="content")

    def get_queryset(self):
        user = self.get_user()
        queryset = Content.objects.filter(user=user)
        if user != self.request.user:
            return queryset.filter(status="ready")
        return queryset


class Comment(UserMixin):
    "user's comment page"
    template_name = "users/history/comment.html"
    extra_context = dict(tab="comment", user_comment=True)

    def get_queryset(self):
        user = self.get_user()
        return ThreadedComments.objects.filter(to=user).exclude(user=user)


class Bookmark(UserMixin):
    template_name = "users/bookmark/index.html"
    extra_context = dict(tab="bookmark")

    def get_queryset(self):
        return BookmarkModel.objects.filter(user=self.get_user()).order_by("-id")


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
                "We've deleted all your information and permanently flagged your account. Your account has been deleted.",
            )
            return redirect("/")
        messages.warning(request, "Your username does not match.")
        return render(
            request, self.template_name, dict(form=self.form_class(data=request.POST))
        )
