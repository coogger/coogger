from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django_bookmark.models import Bookmark
from django_vote_system.models import Vote
from djangobadge.models import UserBadge

from ....threaded_comment.models import ThreadedComments
from ...forms import UsernameForm
from ...models import Commit, Issue, UTopic


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
        if user == request.user or request.user.is_superuser:
            ghost_user = User.objects.get(username="ghost")
            # user topic, content, commit, issues
            UTopic.objects.filter(user=user).delete()
            # comment TODO make update acording to delete and write this message 'this account has been deleted'
            ThreadedComments.objects.filter(user=user).delete()
            # vote
            Vote.objects.filter(user=user).delete()
            # badge
            UserBadge.objects.filter(user=user).delete()
            # bookmark
            for bookmark in Bookmark.objects.filter(user=user):
                bookmark.user.remove(user)
            # follow delete
            for follow_user in user.follow.following.all():
                user.follow.following.remove(follow_user)
            for following_user in user.following.all():
                user.following.remove(following_user)
            Issue.objects.filter(user=user).update(user=ghost_user)
            Commit.objects.filter(user=user).update(user=ghost_user)
            user.is_active = False
            user.first_name = ""
            user.last_name = ""
            user.email = ""
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
