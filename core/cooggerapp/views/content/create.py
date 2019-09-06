from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View

from ...forms import ContentCreateForm
from ...models import Category, Commit, Content, UTopic
from .utils import redirect_utopic


class Create(LoginRequiredMixin, View):
    # TODO use createview class as inherit
    template_name = "content/post/create.html"
    form_class = ContentCreateForm

    def get(self, request, utopic_permlink, *args, **kwargs):
        self.initial, category = dict(), None
        if not UTopic.objects.filter(
            user=request.user, permlink=utopic_permlink
        ).exists():
            return redirect_utopic(request, utopic_permlink)
        for key, value in request.GET.items():
            if key == "category":
                self.initial[key] = Category.objects.get(name=value)
                continue
            self.initial[key] = value
        if "body" not in self.initial:
            self.initial["body"] = self.get_body_template(request)
        return render(
            request,
            self.template_name,
            dict(
                form=self.form_class(
                    initial=self.initial
                )
            )
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

    def get_body_template(self, request):
        category_name = request.GET.get("category", None)
        if category_name is None:
            return render_to_string("content/post/editor-note.html")
        self.initial["category"] = Category.objects.get(name=category_name)
        return self.initial["category"].template
        
