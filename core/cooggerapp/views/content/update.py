from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import slugify
from django.views import View

from ...forms import ContentUpdateForm
from ...models import Commit, Content, UTopic
from ..utils import create_redirect
from .utils import redirect_utopic


class Update(LoginRequiredMixin, View):
    # TODO use updateview class as inherit
    template_name = "content/post/create.html"
    form_class = ContentUpdateForm
    model = Content
    fields = form_class._meta.fields

    def request_permission(self, request, username):
        return request.user.username == username

    def get(self, request, username, permlink, *args, **kwargs):
        if self.request_permission(request, username):
            utopic_permlink = request.GET.get("utopic_permlink", None)
            if (
                utopic_permlink is not None
                and not UTopic.objects.filter(
                    user__username=username, permlink=utopic_permlink
                ).exists()
            ):
                return redirect_utopic(request, utopic_permlink)
            queryset = self.model.objects.filter(
                user__username=username, permlink=permlink
            )
            if queryset.exists():
                form_set = self.form_class(
                    instance=queryset[0],
                    initial=dict(msg=f"Update {queryset[0].title.lower()}"),
                )
                context = dict(username=username, permlink=permlink, form=form_set)
                return render(request, self.template_name, context)
        return HttpResponse(status=403)

    def post(self, request, username, permlink, *args, **kwargs):
        if self.request_permission(request, username):
            queryset = get_object_or_404(
                self.model, user__username=username, permlink=permlink
            )
            form = self.form_class(data=request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                utopic = UTopic.objects.get(id=queryset.utopic.id)
                utopic.commit_count += 1
                if form.body != queryset.body:
                    Commit(
                        user=request.user,
                        utopic=utopic,
                        content=queryset,
                        body=form.body,
                        msg=request.POST.get("msg"),
                    ).save()
                try:
                    self.fields.remove("status")
                except ValueError:
                    pass
                for field in self.fields:
                    setattr(queryset, field, getattr(form, field, None))
                if queryset.status != form.status:
                    queryset.status = form.status
                    self.fields.append("status")
                if queryset.permlink != slugify(queryset.title):
                    self.fields.append("permlink")
                    create_redirect(
                        old_path=reverse(
                            "content-detail",
                            kwargs=dict(username=username, permlink=permlink),
                        ),
                        new_path=reverse(
                            "content-detail",
                            kwargs=dict(
                                username=username, permlink=slugify(queryset.title)
                            ),
                        ),
                    )
                queryset.save(update_fields=self.fields)
                return redirect(queryset.get_absolute_url)
            return render(
                request,
                self.template_name,
                dict(form=form, username=username, permlink=permlink),
            )
