#django
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.contrib import messages as ms
from django.db.models import F

# class
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

#models
from cooggerapp.models import OtherInformationOfUsers,Content

#forms
from cooggerapp.forms import AboutForm

#views
from cooggerapp.views.tools import get_facebook,users_web,paginator

# steem
from steem import Steem

#python
import os
import json
import requests

# sc2py.
from sc2py.sc2py import Sc2
from sc2py import operations

class UserClassBased(TemplateView): # TODO: users who are not signed in can not be displayed
    "herhangi kullanıcının anasayfası"
    template_name = "users/user.html"
    ctof = Content.objects.filter
    title = "{} | coogger"
    keywords = "{},{} {}"
    description = "{} {},{} adı ile coogger'da"

    def get_context_data(self, username, **kwargs):
        user = User.objects.filter(username = username)[0]
        queryset = self.ctof(community = self.request.community_model,user = user,status = "approved")
        info_of_cards = paginator(self.request,queryset)
        context = super(UserClassBased, self).get_context_data(**kwargs)
        nav_category = []
        for i in queryset:
            c_list = i.topic
            if c_list not in nav_category:
                nav_category.append(c_list)
        context["content"] = info_of_cards
        context["content_user"] = User.objects.filter(username = username)[0]
        context["user_follow"] = users_web(user)
        context["nav_category"] = nav_category
        context["head"] = self.html_head(username,user)
        return context

    def html_head(self, username,user):
        html_head = dict(
         title = self.title.format(username),
         keywords = self.keywords.format(username,user.first_name,user.last_name),
         description = self.description.format(user.first_name,user.last_name,username),
         author = get_facebook(user),
        )


class UserTopic(UserClassBased):
    "kullanıcıların konu adresleri"
    keywords = "{} {},{}"
    description = "{} kullanıcımızın {} adlı içerik listesi"

    def get_context_data(self, utopic, username, **kwargs):
        context = super(UserTopic, self).get_context_data(username,**kwargs)
        user = context["content_user"]
        queryset = self.ctof(community = self.request.community_model,user = user,topic = utopic,status = "approved")
        info_of_cards = paginator(self.request,queryset)
        html_head = dict(
         title = self.title.format(username+" - "+utopic),
         keywords = self.keywords.format(username,utopic,utopic),
         description = self.description.format(username,utopic),
         author = get_facebook(user),
        )
        context["user_follow"] = users_web(user)
        context["head"] = html_head
        context["nameoftopic"] = utopic
        context["content"] = info_of_cards
        return context


class UserAboutBaseClass(View):
    template_name = "users/user.html"
    form_class = AboutForm
    oiouof = OtherInformationOfUsers.objects.filter
    title = "{} hakkında | coogger"
    keywords = "{} hakkında"
    description = "{} hakkında | coogger"

    def get(self, request, username, *args, **kwargs):
        user = User.objects.filter(username = username)[0]
        query = self.oiouof(user = user)[0]
        if user == request.user:
            about_form = self.form_class(request.GET or None,instance=query)
        else:
            about_form = query.about
        queryset = Content.objects.filter(user = user)
        nav_category = []
        for i in queryset:
            c_list = i.topic
            if c_list not in nav_category:
                nav_category.append(c_list)
        html_head = dict(
         title = self.title.format(username),
         keywords = self.keywords.format(username),
         description = self.description.format(username),
         author = get_facebook(user),
        )
        context = {}
        context["about"] = about_form
        context["true_about"] = True
        context["content_user"] = user
        context["user_follow"] = users_web(user)
        context["nav_category"] = nav_category
        context["head"] = html_head
        return render(request,self.template_name,context)

    def post(self, request, username, *args, **kwargs):
        if request.user.is_authenticated: # oturum açmış ve
            if request.user.username == username: # kendisi ise
                query = self.oiouof(user = request.user)[0]
                about_form = self.form_class(request.POST,instance=query)
                if about_form.is_valid(): # ve post isteği ise
                    about_form = about_form.save(commit = False)
                    about_form.user = request.user
                    about_form.about = "\n" + about_form.about
                    about_form.save()
                    return HttpResponseRedirect("/web/about/@{}".format(request.user.username))


class FollowBaseClass(View): # TODO: in here do steemconnect js

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            which_user = request.POST["which_user"]
            user_obj = User.objects.filter(username = which_user)[0]
            if user_obj != request.user:
                followers_num = 0# OtherInformationOfUsers(user = user_obj).following_count
                if user_obj.username in self.steem_following(username = request.user.username):
                    self.unfollow(request,request.user.username,user_obj.username)
                    return HttpResponse(json.dumps({"ms":"Follow","num":followers_num -1 }))
                self.follow(request,request.user.username,user_obj.username)
                return HttpResponse(json.dumps({"ms":"Following","num":followers_num + 1 }))

    @staticmethod
    def get_token(request):
        access_token = SteemConnectUser.objects.filter(user = request.user)[0].access_token
        return str(access_token)

    def follow(self,request,user,which_user):
        followjson = operations.Follow(user,which_user).json
        data = operations.Operations(json = followjson).json
        Sc2(token = self.get_token(request),data = data).run

    def unfollow(self,request,user,which_user):
        unjson = operations.Unfollow(user,which_user).json
        data = operations.Operations(json = unjson).json
        Sc2(token = self.get_token(request),data = data).run

    def steem_following(username): # TODO: fixed this section,limit = 100 ?
        STEEM = Steem(nodes=['https://api.steemit.com'])
        return [i["following"] for i in STEEM.get_following(username, 'abit', 'blog',limit = 100)]
