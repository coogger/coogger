from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import slugify
from django.views import View
from django.views.generic import TemplateView

from ...forms import UTopicForm
from ...models import Content, Topic, UTopic
from ..user.users import Common
from ..utils import paginator


class UserTopic(Common):
    template_name = "users/topic/index.html"

    def get_context_data(self, username, **kwargs):
        context = super().get_context_data(username, **kwargs)
        user = context["current_user"]
        context["queryset"] = paginator(self.request, UTopic.objects.filter(user=user))
        return context


class DetailUserTopic(TemplateView):
    "topic/@username"
    template_name = "users/topic/detail/contents.html"

    def get_context_data(self, username, permlink, **kwargs):
        user = get_object_or_404(User, username=username)
        utopic = UTopic.objects.get(user=user, permlink=permlink)
        queryset = Content.objects.filter(utopic=utopic).order_by("created")
        context = super().get_context_data(**kwargs)
        context["current_user"] = user
        context["queryset"] = queryset
        context["utopic"] = utopic
        return context


class CreateUTopic(LoginRequiredMixin, View):
    template_name = "forms/create.html"
    form_class = UTopicForm
    model = UTopic

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            dict(form=self.form_class(initial=dict(request.GET.items()))),
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            try:
                form.save()
            except IntegrityError:
                messages.warning(
                    request, f"{form.name.lower()} is already taken by yours"
                )
                return render(
                    request,
                    self.template_name,
                    dict(form=self.form_class(data=request.POST)),
                )
            return redirect(
                reverse(
                    "detail-utopic",
                    kwargs=dict(permlink=form.permlink, username=str(form.user)),
                )
            )
        return render(request, self.template_name, dict(form=form))


class UpdateUTopic(LoginRequiredMixin, View):
    template_name = "forms/create.html"
    form_class = UTopicForm
    model = UTopic

    def get(self, request, permlink, *args, **kwargs):
        instance_query = self.model.objects.filter(user=request.user, permlink=permlink)
        if not instance_query.exists():
            messages.warning(request, f"you need to create the {permlink} topic first.")
            return redirect(reverse("create-utopic") + f"?name={permlink}")
        context = dict(
            form=self.form_class(instance=instance_query[0]), permlink=permlink
        )
        return render(request, self.template_name, context)

    def post(self, request, permlink, *args, **kwargs):
        form = self.form_class(data=request.POST)
        context = dict(form=form, permlink=permlink)
        if form.is_valid():
            form = form.save(commit=False)
            self.model.objects.filter(user=request.user, permlink=permlink).update(
                name=form.name,
                permlink=slugify(form.name),
                image_address=form.image_address,
                definition=form.definition,
                tags=form.tags,
                address=form.address,
            )
            if permlink != slugify(form.name):
                # new global topic save
                if (
                    not Content.objects.filter(utopic__permlink=permlink).exists()
                    and not UTopic.objects.filter(permlink=permlink).exists()
                ):
                    Topic.objects.filter(permlink=permlink).update(
                        permlink=slugify(form.name)
                    )
                else:
                    try:
                        Topic(name=form.name.lower()).save()
                    except IntegrityError:
                        pass
            return redirect(
                reverse(
                    "detail-utopic",
                    kwargs=dict(
                        permlink=slugify(form.name), username=str(request.user)
                    ),
                )
            )
        return render(request, self.template_name, context)
