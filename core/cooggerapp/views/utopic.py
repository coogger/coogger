# django
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth.models import User
from django.db import IntegrityError

# model
from ..models import (Topic, UTopic, Content, Commit)

# form
from ..forms import UTopicForm


class UserTopic(TemplateView):
    "topic/@username"
    template_name = "utopic/contents-for-alt.html"

    def get_context_data(self, username, permlink, **kwargs):
        user = User.objects.get(username=username)
        utopic = UTopic.objects.get(user=user, permlink=permlink)
        contents = Content.objects.filter(
            user=user, 
            utopic=utopic, 
            status="approved", 
            reply=None).order_by("created")
        commits = Commit.objects.filter(utopic=utopic)
        context = super().get_context_data(**kwargs)
        if commits.exists():
            context["last_commit_created"] = commits[0].created        
        context["current_user"] = user
        context["queryset"] = contents
        context["utopic"] = utopic
        return context


class CreateUTopic(LoginRequiredMixin, View):
    template_name = "post/utopic.html"
    form_class = UTopicForm
    model = UTopic

    def get(self, request, *args, **kwargs):
        return render(
            request, 
            self.template_name, 
            dict(
                form=self.form_class(
                    initial=dict(
                        request.GET.items()
                    )
                )
            )
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            if not self.model.objects.filter(user=request.user, name=form.name).exists():
                save = form.save()
                return redirect(
                    reverse(
                        "utopic", 
                        kwargs=dict(
                            permlink=form.permlink, 
                            username=str(form.user)
                        )
                    )
                )
            else:
                messages.warning(request, f"{form.name} is already taken by yours" )
                return render(request, self.template_name, dict(form=self.form_class(data=request.POST)))
        else:
            return render(request, self.template_name, dict(form=form))


class UpdateUTopic(LoginRequiredMixin, View):
    template_name = "post/updateutopic.html"
    form_class = UTopicForm
    model = UTopic

    def get(self, request, permlink, *args, **kwargs):
        try:
            instance = self.model.objects.filter(user=request.user, permlink=permlink)[0]
        except IndexError:
            messages.warning(request, f"you need to create the {value} topic first.")
            return redirect(reverse("create-utopic")+"?name={value}")
        context = dict(
            form=self.form_class(instance=instance),
            permlink=permlink
        )
        return render(request, self.template_name, context)

    def post(self, request, permlink, *args, **kwargs):
        form = self.form_class(data=request.POST)
        context = dict(
            form=form,
            permlink=permlink,
        )
        if form.is_valid():
            form = form.save(commit=False)
            self.model.objects.filter(user=request.user, permlink=permlink).update(
                name=form.name,
                image_address=form.image_address,
                definition=form.definition,
                tags=form.tags,
                address=form.address,
            )
            try:
                Topic(name=form.name).save()
            except IntegrityError:
                pass
            return redirect(
                    reverse(
                        "utopic", 
                        kwargs=dict(
                            permlink=permlink, 
                            username=str(request.user)
                        )
                    )
                )
        return render(request, self.template_name, context)
