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
        context = super(Home, self).get_context_data(**kwargs)
        context["content"] = queryset[:settings.PAGE_SIZE]
        context["content_user"] = user
        context["user_follow"] = OtherAddressesOfUsers(user=user).get_addresses
        context["topics"] = UTopic.objects.filter(user=user)
        return context


class Topic(TemplateView):
    "kullanıcıların konu adresleri"
    template_name = "users/topic/contents-for-alt.html"

    def get_context_data(self, username, topic, **kwargs):
        user = authenticate(username=username)
        try:
            global_topic = TopicModel.objects.filter(name=topic)[0]
        except IndexError:
            contents = list()
        else:
            contents = Content.objects.filter(user=user, topic=global_topic, status="approved")
        try:
            utopic = UTopic.objects.filter(user=user, name=topic)[0]
        except IndexError:
            raise Http404("There is no such topic of this user.")
        commits = Commit.objects.filter(utopic=utopic)
        total_dor = 0
        for dor in [query.dor for query in contents]:
            total_dor += dor
        total_views = 0
        for views in [query.views for query in contents]:
            total_views += views
        try:
            last_commit = commits[len(commits)-1]
        except AssertionError:
            last_commit = list()
        context = super(Topic, self).get_context_data(**kwargs)
        context["content_user"] = user
        context["queryset"] = contents
        context["commits"] = commits
        context["commits_count"] = commits.count()
        context["last_commit"] = last_commit
        context["utopic"] = utopic
        context["total_dor"] = f"{round(total_dor, 3)} min"
        context["total_views"] = total_views
        return context


class About(View):
    template_name = "users/about.html"
    form_class = AboutForm

    def get(self, request, username, *args, **kwargs):
        user = authenticate(username=username)
        try:
            query = OtherInformationOfUsers.objects.filter(user=user)[0]
        except IndexError:
            pass
        else:
            if user == request.user:
                context["about"] = self.form_class(request.GET or None, instance=query)
            else:
                context["about"] = query.about
        queryset = Content.objects.filter(user=user, status="approved")
        context = {}
        context["content_user"] = user
        context["user_follow"] = OtherAddressesOfUsers(user=user).get_addresses
        context["topics"] = UTopic.objects.filter(user=user)
        return render(request, self.template_name, context)

    def post(self, request, username, *args, **kwargs):
        if request.user.is_authenticated:  # oturum açmış ve
            if request.user.username == username:  # kendisi ise
                query = OtherInformationOfUsers.objects.filter(user=request.user)[0]
                about_form = self.form_class(request.POST, instance=query)
                if about_form.is_valid():  # ve post isteği ise
                    about_form = about_form.save(commit=False)
                    about_form.user = request.user
                    about_form.about = "\n" + about_form.about
                    about_form.save()
                    return redirect(reverse("userabout", kwargs=dict(username=request.user.username)))


class Comment(TemplateView):
    "History of users"
    template_name = "users/history/comment.html"

    def get_context_data(self, username, **kwargs):
        context = super(Comment, self).get_context_data(**kwargs)
        user = authenticate(username=username)
        queryset = Content.objects.filter(user=user, status="approved")
        context["user_follow"] = OtherAddressesOfUsers(user=user).get_addresses
        context["content_user"] = user
        context["topics"] = UTopic.objects.filter(user=user)
        context["django_md_editor"] = True
        context["user_comment"] = True
        return context


class Wallet(Comment):
    "History of users"
    template_name = "users/history/wallet.html"

    def get_context_data(self, username, **kwargs):
        context = super(Wallet, self).get_context_data(username, **kwargs)
        return context


class Activity(Comment):
    "History of users"
    template_name = "users/history/activity.html"

    def get_context_data(self, username, **kwargs):
        context = super(Activity, self).get_context_data(username, **kwargs)
        return context
