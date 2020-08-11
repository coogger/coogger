from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import slugify
from django.views import View

from ...forms import ContentUpdateForm
from ...models import Commit, Content, UTopic
from ..utils import create_redirect
from .utils import redirect_utopic


class ReplaceOrder(LoginRequiredMixin, View):
    def post(self, request, *arg, **kwargs):
        object_id = int(request.POST["object_id"])
        to_order = int(request.POST["to_order"])
        copy_to_order = to_order
        from_order = int(request.POST["from_order"])
        contents = {
            content.order: content
            for content in Content.objects.filter(
                user=request.user, utopic__id=object_id
            )
        }
        new_contents = {}
        from_content = contents[from_order]
        del contents[from_order]
        if from_order < to_order:
            op = -1
        else:
            op = +1
        while True:
            try:
                content = contents[to_order]
            except KeyError:
                break
            del contents[to_order]
            new_order = to_order + op
            if new_order == 0:
                break
            new_contents[new_order] = content
            to_order = to_order + op
        new_contents[copy_to_order] = from_content
        for key, value in new_contents.items():
            value.order = key
            value.save()
        return JsonResponse({})


class Update(LoginRequiredMixin, View):
    # TODO use updateview class as inherit
    template_name = "content/post/create.html"
    form_class = ContentUpdateForm
    model = Content
    update_fields = form_class._meta.fields

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
                context = dict(
                    username=username, permlink=permlink, form=form_set
                )
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
                utopic.save()
                if form.body != queryset.body:
                    Commit(
                        user=request.user,
                        utopic=utopic,
                        content=queryset,
                        body=form.body,
                        msg=request.POST.get("msg"),
                    ).save()
                try:
                    self.update_fields.remove("status")
                except ValueError:
                    pass
                for field in self.update_fields:
                    setattr(queryset, field, getattr(form, field, None))
                if queryset.status != form.status:
                    queryset.status = form.status
                    self.update_fields.append("status")
                if queryset.permlink != slugify(queryset.title):
                    self.update_fields.append("permlink")
                    queryset.permlink = queryset.generate_permlink()
                    create_redirect(
                        old_path=reverse(
                            "content-detail",
                            kwargs=dict(username=username, permlink=permlink),
                        ),
                        new_path=reverse(
                            "content-detail",
                            kwargs=dict(
                                username=username, permlink=queryset.permlink
                            ),
                        ),
                    )
                queryset.save(update_fields=self.update_fields)
                return redirect(queryset.get_absolute_url)
            return render(
                request,
                self.template_name,
                dict(form=form, username=username, permlink=permlink),
            )
