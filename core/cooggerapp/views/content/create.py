from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views import View

from ...forms import ContentCreateForm
from ...models import Category, Commit, Content, UTopic
from .utils import redirect_utopic


class Create(LoginRequiredMixin, View):
    # TODO use createview class as inherit
    template_name = "content/post/create.html"
    form_class = ContentCreateForm
    initial_template = "content/post/editor-note.html"

    def get(self, request, utopic_permlink, *args, **kwargs):
        initial, category = dict(), None
        if not UTopic.objects.filter(
            user=request.user, permlink=utopic_permlink
        ).exists():
            return redirect_utopic(request, utopic_permlink)
        for key, value in request.GET.items():
            if key == "category":
                category = Category.objects.get(name=value)
                category_template = category.template
                initial.__setitem__("category", category)
            else:
                initial.__setitem__(key, value)
        if category is None:
            category_template = render_to_string(self.initial_template)
        initial.__setitem__("body", category_template)
        initial.__setitem__("msg", "Initial commit")
        context = dict(form=self.form_class(initial=initial))
        return render(request, self.template_name, context)

    def post(self, request, utopic_permlink, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            user_topic = UTopic.objects.filter(
                user=request.user, permlink=utopic_permlink
            )
            form.user = request.user
            form.utopic = user_topic[0]
            form.tags = ready_tags(form.tags)  # make validation
            form.save()
            return redirect(
                reverse(
                    "content-detail",
                    kwargs=dict(username=str(form.user), permlink=form.permlink),
                )
            )
        return render(request, self.template_name, dict(form=form))
