# django
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.contrib import messages as ms
from django.db.models import F
from django.contrib.auth import authenticate

# class
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# models
from cooggerapp.models import OtherInformationOfUsers, Content

# forms
from cooggerapp.forms import AboutForm

# views
from cooggerapp.views.tools import get_facebook, users_web, paginator, user_topics

# steem
from steem import Steem

# python
import os
import json
import requests


class UserClassBased(TemplateView):
    "user's home page"
    template_name = "users/user.html"
    ctof = Content.objects.filter

    def get_context_data(self, username, **kwargs):
        user = authenticate(username=username)
        if self.request.community_model.name == "coogger":
            queryset = self.ctof(user=user, status="approved")
        else:
            queryset = self.ctof(community=self.request.community_model, user=user, status="approved")
        info_of_cards = paginator(self.request, queryset)
        context = super(UserClassBased, self).get_context_data(**kwargs)
        context["content"] = info_of_cards
        context["content_user"] = User.objects.filter(username=username)[0]
        context["user_follow"] = users_web(user)
        context["topics"] = user_topics(queryset)
        return context


class UserTopic(UserClassBased):
    "kullanıcıların konu adresleri"

    def get_context_data(self, utopic, username, **kwargs):
        context = super(UserTopic, self).get_context_data(username, **kwargs)
        user = context["content_user"]
        if self.request.community_model.name == "coogger":
            queryset = self.ctof(user=user, topic=utopic, status="approved")
        else:
            queryset = self.ctof(community=self.request.community_model, user=user, topic=utopic, status="approved")
        info_of_cards = paginator(self.request, queryset)
        context["user_follow"] = users_web(user)
        context["nameoftopic"] = utopic
        context["content"] = info_of_cards
        return context


class UserAboutBaseClass(View):
    template_name = "users/about.html"
    form_class = AboutForm
    oiouof = OtherInformationOfUsers.objects.filter

    def get(self, request, username, *args, **kwargs):
        user = authenticate(username=username)
        query = self.oiouof(user=user)[0]
        if user == request.user:
            about_form = self.form_class(request.GET or None, instance=query)
        else:
            about_form = query.about
        if self.request.community_model.name == "coogger":
            queryset = Content.objects.filter(user=user, status="approved")
        else:
            queryset = Content.objects.filter(user=user, status="approved", community=request.community_model)
        context = {}
        context["about"] = about_form
        context["content_user"] = user
        context["user_follow"] = users_web(user)
        context["topics"] = user_topics(queryset)
        return render(request, self.template_name, context)

    def post(self, request, username, *args, **kwargs):
        if request.user.is_authenticated:  # oturum açmış ve
            if request.user.username == username:  # kendisi ise
                query = self.oiouof(user=request.user)[0]
                about_form = self.form_class(request.POST, instance=query)
                if about_form.is_valid():  # ve post isteği ise
                    about_form = about_form.save(commit=False)
                    about_form.user = request.user
                    about_form.about = "\n" + about_form.about
                    about_form.save()
                    return HttpResponseRedirect("/about/@{}".format(request.user.username))


class UserHistory(TemplateView):
    "History of users"
    template_name = "users/history.html"

    def get_context_data(self, username, **kwargs):
        context = super(UserHistory, self).get_context_data(**kwargs)
        user = authenticate(username=username)
        if self.request.community_model.name == "coogger":
            queryset = Content.objects.filter(user=user, status="approved")
        else:
            queryset = Content.objects.filter(user=user, status="approved", community=self.request.community_model)
        context["user_follow"] = users_web(user)
        context["content_user"] = user
        context["topics"] = user_topics(queryset)
        return context


class UserWallet(UserHistory):
    "History of users"
    template_name = "users/wallet.html"

    def get_context_data(self, username, **kwargs):
        context = super(UserWallet, self).get_context_data(username, **kwargs)
        return context
