from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from ...forms import ContentUpdateForm
from ...models import Commit, Content, UTopic
from .utils import redirect_utopic


class Update(LoginRequiredMixin, View):
    # TODO use updateview class as inherit
    template_name = "content/post/update.html"
    form_class = ContentUpdateForm
    model = Content
    fields = form_class._meta.fields.remove("status")

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
                get_utopic_permlink = request.GET.get("utopic_permlink", None)
                if get_utopic_permlink is None:
                    utopic = queryset.utopic
                else:
                    utopic = UTopic.objects.filter(  # new utopic
                        user=queryset.user, permlink=get_utopic_permlink
                    )
                    utopic.update(  # new utopic update
                        how_many=(F("how_many") + 1),
                        total_dor=(F("total_dor") + dor(form.body)),
                        total_view=(F("total_view") + queryset.views),
                    )
                    UTopic.objects.filter(  # old utopic update
                        user=queryset.user, permlink=queryset.utopic.permlink
                    ).update(
                        how_many=(F("how_many") - 1),
                        total_dor=(F("total_dor") - dor(queryset.body)),
                        total_view=(F("total_view") - queryset.views),
                    )
                    utopic = utopic[0]
                    Commit.objects.filter(  # old utopic update to new utopic commit
                        utopic=queryset.utopic, content=queryset
                    ).update(utopic=utopic)
                if form.body != queryset.body:
                    Commit(
                        user=request.user,
                        utopic=utopic,
                        content=queryset,
                        body=form.body,
                        msg=request.POST.get("msg"),
                    ).save()
                for field in self.fields:
                    setattr(queryset, field, getattr(form, field, None))
                if queryset.status != form.status:
                    queryset.status = form.status
                    self.fields.append("status")
                queryset.utopic = utopic
                queryset.save(update_fields=self.fields)  # to content signals
                return redirect(
                    reverse(
                        "content-detail",
                        kwargs=dict(
                            username=str(queryset.user), permlink=queryset.permlink
                        ),
                    )
                )
            context = dict(form=form, username=username, permlink=permlink)
            return render(request, self.template_name, context)
