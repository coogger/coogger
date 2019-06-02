# django
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

# models
from core.cooggerapp.models import Content, Category, UTopic, Topic

# form
from core.cooggerapp.forms import ContentForm, ReplyForm


class Create(LoginRequiredMixin, View):
    template_name = "post/create.html"
    form_class = ContentForm
    initial_template = "post/editor-note.html"

    def get(self, request, utopic_permlink, *args, **kwargs):
        initial, category = dict(), None
        if not UTopic.objects.filter(user=request.user, permlink=utopic_permlink).exists():
            messages.warning(request, f"you need to create the {utopic_permlink} topic first.")
            return redirect(reverse("create-utopic")+f"?name={utopic_permlink}")
        for key, value in request.GET.items():
            if key == "category":
                category = Category.objects.get(name=value)
                category_template = category.template
                initial.__setitem__("category", category)
            elif key == "topic":
                try:
                    utopic = UTopic.objects.filter(user=request.user, name=value)[0]
                except IndexError:
                    messages.warning(request, f"you need to create the {value} topic first.")
                    return redirect(reverse("create-utopic")+f"?name={value}")
                initial.__setitem__("topic", utopic)
            else:
                initial.__setitem__(key, value)
        if category is None:
            category_template = render_to_string(self.initial_template)
        initial.__setitem__("body", category_template)
        initial.__setitem__("msg", "Initial commit")
        context = dict(
            form=self.form_class(initial=initial)
        )
        return render(request, self.template_name, context)

    def post(self, request, utopic_permlink, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            save = form.content_save(request, form, utopic_permlink)
            return redirect(reverse("detail", kwargs=dict(username=str(form.user), permlink=form.permlink)))
        return render(request, self.template_name, dict(form=form))


class Change(LoginRequiredMixin, View):
    template_name = "post/change.html"
    form_class = ContentForm
    reply_form_class = ReplyForm
    model = Content

    def get(self, request, username, permlink, *args, **kwargs):
        if request.user.username == username:
            utopic_permlink = request.GET.get("utopic_permlink", None)
            if utopic_permlink is not None and not UTopic.objects.filter(
                user=request.user, permlink=utopic_permlink).exists():
                messages.warning(request, f"you need to create the {utopic_permlink} topic first.")
                return redirect(reverse("create-utopic")+f"?name={utopic_permlink}")
            queryset = self.model.objects.filter(user=request.user, permlink=permlink)
            if queryset.exists():
                if queryset[0].reply is not None:
                    form_set = self.reply_form_class(instance=queryset[0])
                else:
                    form_set = self.form_class(instance=queryset[0], initial=dict(msg=f"Update {queryset[0].title.lower()}"))
                context = dict(
                    username=username,
                    permlink=permlink,
                    form=form_set,
                )
                return render(request, self.template_name, context)
        raise Http404

    def post(self, request, username, permlink, *args, **kwargs):
        if request.user.username == username:
            queryset = self.model.objects.filter(user=request.user, permlink=permlink)
            if queryset.exists():
                if queryset[0].reply is not None:
                    form = self.reply_form_class(data=request.POST)
                else:
                    form = self.form_class(data=request.POST)
                if form.is_valid():
                    form = form.save(commit=False)
                    save = form.content_update(request=request, old=queryset, new=form)
                    return redirect(
                        reverse(
                            "detail", 
                            kwargs=dict(
                                username=str(queryset[0].user), 
                                permlink=queryset[0].permlink
                                )
                            )
                        )
                else:
                    context = dict(
                        form=form,
                        username=username,
                        permlink=permlink
                    )
                    return render(request, self.template_name, context)
