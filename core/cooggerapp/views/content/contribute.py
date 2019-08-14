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
                    commit, c_created = Commit.objects.get_or_create(
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
            context = dict(form=form, username=username, permlink=permlink)
            return render(request, self.template_name, context)


class ApproveContribute(LoginRequiredMixin, View):
    get_status = "approved"

    def get(self, request, username, topic_permlink, hash):
        commit = get_object_or_404(Commit, hash=hash)
        if str(request.user) == commit.utopic.user and commit.status == "waiting":
            if commit.status != self.get_status:
                content = Content.objects.get(id=commit.content.id)
                content.body = commit.body
                content.save()
                commit.status = self.get_status
                commit.save()
                self.update_utopic(UTopic.objects.get(id=commit.utopic.id))
            else:
                messages.warning(request, "You can not change this commit")
            return redirect(
                reverse(
                    "content-detail",
                    kwargs=dict(username=content.user, permlink=content.permlink),
                )
            )

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
            return redirect(
                reverse(
                    "content-detail",
                    kwargs=dict(
                        username=commit.content.user, permlink=commit.content.permlink
                    ),
                )
            )
