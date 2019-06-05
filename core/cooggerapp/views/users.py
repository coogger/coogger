# django
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .utils import paginator

# class
from django.views.generic.base import TemplateView
from django.views import View

# models
from ..models import (UserProfile, Content,  UTopic)

# forms
from ..forms import AboutForm

# utils 
from .utils import paginator


class Home(TemplateView):
    "user's home page"
    template_name = "users/user.html"

    def get_context_data(self, username, **kwargs):
        user = User.objects.get(username=username)
        queryset = Content.objects.filter(user=user, status="approved", reply=None)
        context = super().get_context_data(**kwargs)
        context["queryset"] = paginator(self.request, queryset)
        context["current_user"] = user
        context["addresses"] = UserProfile.objects.get(user=user).address.all()
        context["topics"] = UTopic.objects.filter(user=user)[:6]
        return context


class About(View):
    template_name = "users/about.html"
    form_class = AboutForm

    def get(self, request, username, *args, **kwargs):
        context = {}
        user = User.objects.get(username=username)
        try:
            query = UserProfile.objects.filter(user=user)[0]
        except IndexError:
            query = []
        else:
            if user == request.user:
                context["about"] = self.form_class(request.GET or None, instance=query)
            else:
                context["about"] = query.about
        context["current_user"] = user
        context["addresses"] = UserProfile.objects.get(user=user).address.all()
        context["topics"] = UTopic.objects.filter(user=user)[:6]
        context["md_editor"] = True
        return render(request, self.template_name, context)

    def post(self, request, username, *args, **kwargs):
        if request.user.is_authenticated and \
            request.user.username == username:
            query = UserProfile.objects.filter(user=request.user)[0]
            about_form = self.form_class(request.POST, instance=query)
            if about_form.is_valid():
                about_form = about_form.save(commit=False)
                about_form.user = request.user
                about_form.about = "\n" + about_form.about
                about_form.save()
                return redirect(reverse("userabout", kwargs=dict(username=request.user.username)))


class Activity(TemplateView):
    "History of users"
    template_name = "users/history/activity.html"

    def get_context_data(self, username, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=username)
        context["addresses"] = UserProfile.objects.get(user=user).address.all()
        context["current_user"] = user
        context["topics"] = UTopic.objects.filter(user=user)[:6]
        return context


class Comment(Activity):
    "History of users"
    template_name = "users/history/comment.html"

    def get_context_data(self, username, **kwargs):
        context = super().get_context_data(username, **kwargs)
        user = context["current_user"]
        queryset = Content.objects.filter(
            status="approved"
            ).exclude(
                user=user
                ).filter(
                    reply__user=user
                    )
        context["md_editor"] = True
        context["user_comment"] = True
        context["queryset"] = paginator(self.request, queryset)
        return context