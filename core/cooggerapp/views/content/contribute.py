from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from ...forms import ContentContributeForm
from ...models import Category, Commit, Content, UTopic
from .update import Update


class Contribute(Update):
    form_class = ContentContributeForm

    def request_permission(self, request, username):
        return request.user.is_authenticated and str(request.user) != username

    def post(self, request, username, permlink, *args, **kwargs):
        if self.request_permission(request, username):
            queryset = get_object_or_404(
                self.model, user__username=username, permlink=permlink
            )
            form = self.form_class(data=request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                utopic = queryset.utopic
                if form.body != queryset.body:
                    # NOTE get_or_create to use create and get obj
                    commit, _ = Commit.objects.get_or_create(
                        user=request.user,
                        utopic=utopic,
                        content=queryset,
                        body=form.body,
                        msg=request.POST.get("msg"),
                        status="waiting",
                    )
                    return redirect(
                        reverse(
                            "commit",
                            kwargs=dict(
                                username=str(request.user),
                                topic_permlink=utopic.permlink,
                                hash=commit.hash,
                            ),
                        )
                    )
            messages.warning(
                request, "Something went wrong.. we could not do this contribute."
            )
            return redirect(
                reverse(
                    "content-contribute",
                    kwargs=dict(username=username, permlink=permlink),
                )
            )


class ApproveContribute(LoginRequiredMixin, View):
    get_status = "approved"

    def get(self, request, username, topic_permlink, hash):
        commit = get_object_or_404(Commit, hash=hash)
        if request.user == commit.utopic.user and commit.status == "waiting":
            if commit.status != self.get_status:
                # content
                content = Content.objects.get(id=commit.content.id)
                content.body = commit.body
                # commit
                commit.status = self.get_status
                # utopic
                utopic = UTopic.objects.get(id=commit.utopic.id)
                utopic.commit_count += 1
                if not utopic.contributors.filter(username=str(commit.user)).exists():
                    utopic.contributors_count += 1
                    utopic.contributors.add(commit.user)
                # content
                if not content.contributors.filter(username=str(commit.user)).exists():
                    content.contributors_count += 1
                    content.contributors.add(commit.user)
                content.save()
                commit.save()
                self.update_utopic(utopic)
            else:
                messages.warning(request, "You can not change this commit")
            return redirect(content.get_absolute_url)

    def update_utopic(self, utopic):
        utopic.closed_contribution += 1
        utopic.open_contribution -= 1
        utopic.save()


class RejectContribute(ApproveContribute):
    get_status = "rejected"

    def get(self, request, username, topic_permlink, hash):
        commit = get_object_or_404(Commit, hash=hash)
        if str(request.user) == commit.utopic.user and commit.status == "waiting":
            if commit.status != self.get_status:
                commit.status = self.get_status
                commit.save()
                self.update_utopic(utopic=UTopic.objects.get(id=commit.utopic.id))
            return redirect(commit.content.get_absolute_url)
