from django.shortcuts import get_object_or_404, redirect, render
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
