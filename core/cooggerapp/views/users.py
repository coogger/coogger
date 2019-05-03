# django
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.urls import reverse
from django.conf import settings
from django.http import Http404

# class
from django.views.generic.base import TemplateView
from django.views import View

# models
from core.cooggerapp.models import OtherInformationOfUsers, Content, OtherAddressesOfUsers, Commit, UTopic
from core.cooggerapp.models import Topic as TopicModel

# forms
from core.cooggerapp.forms import AboutForm


class Home(TemplateView):
    "user's home page"
    template_name = "users/user.html"

    def get_context_data(self, username, **kwargs):
        user = authenticate(username=username) # this line for creating new user
        queryset = Content.objects.filter(user=user, status="approved")
        context = super().get_context_data(**kwargs)
        context["content"] = queryset[:settings.PAGE_SIZE]
        context["content_user"] = user
        context["user_follow"] = OtherAddressesOfUsers(user=user).get_addresses
        context["topics"] = UTopic.objects.filter(user=user)
        return context


class Topic(TemplateView):
    "topic/@username"
    template_name = "users/topic/contents-for-alt.html"

    def get_context_data(self, username, topic, **kwargs):
        user = authenticate(username=username)
        global_topic = TopicModel.objects.filter(name=topic)[0]
        contents = Content.objects.filter(user=user, 
            topic=global_topic, status="approved").order_by("created")
        utopic = UTopic.objects.filter(user=user, name=topic)[0]
        commits = Commit.objects.filter(utopic=utopic)
        last_commit_created = commits[0].created
        context = super().get_context_data(**kwargs)
        context["content_user"] = user
        context["queryset"] = contents
        context["commits"] = commits
        context["commits_count"] = commits.count()
        context["last_commit_created"] = last_commit_created
        context["utopic"] = utopic
        context["total_dor"] = self.calculate_dor(contents)
        context["total_views"] = self.calculate_view(contents)
        return context

    def calculate_dor(self, contents):
        total_dor = 0
        for dor in [query.dor for query in contents]: #TODO create new model field for this op
            total_dor += dor
        return f"{round(total_dor, 3)} min"

    def calculate_view(self, contents):
        total_views = 0
        for views in [query.views for query in contents]: #TODO create new model field for this op
            total_views += views
        return total_views


class About(View):
    template_name = "users/about.html"
    form_class = AboutForm

    def get(self, request, username, *args, **kwargs):
        context = {}
        user = authenticate(username=username)
        try:
            query = OtherInformationOfUsers.objects.filter(user=user)[0]
        except IndexError:
            query = []
        else:
            if user == request.user:
                context["about"] = self.form_class(request.GET or None, instance=query)
            else:
                context["about"] = query.about
        queryset = Content.objects.filter(user=user, status="approved")
        context["content_user"] = user
        context["user_follow"] = OtherAddressesOfUsers(user=user).get_addresses
        context["topics"] = UTopic.objects.filter(user=user)
        context["md_editor"] = True
        return render(request, self.template_name, context)

    def post(self, request, username, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.username == username:
                query = OtherInformationOfUsers.objects.filter(user=request.user)[0]
                about_form = self.form_class(request.POST, instance=query)
                if about_form.is_valid():
                    about_form = about_form.save(commit=False)
                    about_form.user = request.user
                    about_form.about = "\n" + about_form.about
                    about_form.save()
                    return redirect(reverse("userabout", kwargs=dict(username=request.user.username)))


class Wallet(TemplateView):
    "History of users"
    template_name = "users/history/wallet.html"

    def get_context_data(self, username, **kwargs):
        context = super().get_context_data(**kwargs)
        user = authenticate(username=username)
        context["user_follow"] = OtherAddressesOfUsers(user=user).get_addresses
        context["content_user"] = user
        return context


class Activity(Wallet):
    "History of users"
    template_name = "users/history/activity.html"

    def get_context_data(self, username, **kwargs):
        context = super().get_context_data(username, **kwargs)
        return context


class Comment(Wallet):
    "History of users"
    template_name = "users/history/comment.html"

    def get_context_data(self, username, **kwargs):
        context = super().get_context_data(username, **kwargs)
        user = context["content_user"]
        queryset = Content.objects.filter(user=user, status="approved")
        context["topics"] = UTopic.objects.filter(user=user)
        context["django_md_editor"] = True
        context["user_comment"] = True
        return context