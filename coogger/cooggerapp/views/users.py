# django
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate

# class
from django.views.generic.base import TemplateView
from django.views import View

# models
from cooggerapp.models import OtherInformationOfUsers, Content

# forms
from cooggerapp.forms import AboutForm

# views
from cooggerapp.views.tools import users_web, paginator, user_topics


class UserClassBased(TemplateView):
    "user's home page"
    template_name = "users/user.html"
    ctof = Content.objects.filter

    def get_context_data(self, username, **kwargs):
        user = authenticate(username=username) # this line for creating new user
        if self.request.dapp_model.name == "coogger":
            queryset = Content.objects.filter(user=user, status="approved")
        else:
            queryset = Content.objects.filter(dapp=self.request.dapp_model, user=user, status="approved")
        info_of_cards = paginator(self.request, queryset)
        context = super(UserClassBased, self).get_context_data(**kwargs)
        context["content"] = info_of_cards
        context["content_user"] = user
        context["user_follow"] = users_web(user)
        context["topics"] = user_topics(queryset)
        return context


class UserTopic(View):
    "kullanıcıların konu adresleri"

    def get(self, request, utopic, username):
        user = authenticate(username=username)
        if request.dapp_model.name == "coogger":
            queryset = Content.objects.filter(user=user, topic=utopic, status="approved")
        else:
            queryset = Content.objects.filter(dapp=request.dapp_model, user=user, topic=utopic, status="approved")
        queryset = queryset.order_by("id")
        return redirect(f"/@{queryset[0].user}/{queryset[0].permlink}")


class UserAboutBaseClass(View):
    template_name = "users/about.html"
    form_class = AboutForm

    def get(self, request, username, *args, **kwargs):
        user = authenticate(username=username)
        query = OtherInformationOfUsers.objects.filter(user=user)[0]
        if user == request.user:
            about_form = self.form_class(request.GET or None, instance=query)
        else:
            about_form = query.about
        if self.request.dapp_model.name == "coogger":
            queryset = Content.objects.filter(user=user, status="approved")
        else:
            queryset = Content.objects.filter(user=user, status="approved", dapp=request.dapp_model)
        context = {}
        context["about"] = about_form
        context["content_user"] = user
        context["user_follow"] = users_web(user)
        context["topics"] = user_topics(queryset)
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
                    return redirect("/about/@{}".format(request.user.username))


class UserComment(TemplateView):
    "History of users"
    template_name = "users/history/comment.html"

    def get_context_data(self, username, **kwargs):
        context = super(UserComment, self).get_context_data(**kwargs)
        user = authenticate(username=username)
        if self.request.dapp_model.name == "coogger":
            queryset = Content.objects.filter(user=user, status="approved")
        else:
            queryset = Content.objects.filter(user=user, status="approved", dapp=self.request.dapp_model)
        context["user_follow"] = users_web(user)
        context["content_user"] = user
        context["topics"] = user_topics(queryset)
        context["django_md_editor"] = True
        return context


class UserWallet(UserComment):
    "History of users"
    template_name = "users/history/wallet.html"

    def get_context_data(self, username, **kwargs):
        context = super(UserWallet, self).get_context_data(username, **kwargs)
        return context


class UserActivity(UserComment):
    "History of users"
    template_name = "users/history/activity.html"

    def get_context_data(self, username, **kwargs):
        context = super(UserActivity, self).get_context_data(username, **kwargs)
        return context
