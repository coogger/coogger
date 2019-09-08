from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View

from ...forms import ContentCreateForm
from ...models import UTopic
from .utils import redirect_utopic


class Create(LoginRequiredMixin, View):
    # TODO use createview class as inherit
    template_name = "content/post/create.html"
    form_class = ContentCreateForm

    def get(self, request, utopic_permlink, *args, **kwargs):
        self.initial = dict()
        if not UTopic.objects.filter(
            user=request.user, permlink=utopic_permlink
        ).exists():
            return redirect_utopic(request, utopic_permlink)
        for key, value in request.GET.items():
            self.initial[key] = value
        if "body" not in self.initial:
            self.initial["body"] = render_to_string("content/post/editor-note.html")
        return render(
            request,
            self.template_name,
            dict(form=self.form_class(initial=self.initial)),
        )

    def post(self, request, utopic_permlink, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.utopic = UTopic.objects.get(
                user=request.user, permlink=utopic_permlink
            )
            form.save()
            return redirect(
                reverse(
                    "content-detail",
                    kwargs=dict(username=str(form.user), permlink=form.permlink),
                )
            )
        return render(request, self.template_name, dict(form=form))
