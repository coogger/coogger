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
from apps.cooggerapp.models import OtherInformationOfUsers,Content,Following

#forms
from apps.cooggerapp.forms import AboutForm

#views
from apps.cooggerapp.views.tools import get_facebook,users_web,paginator

#python
import os
import json
import requests

class UserClassBased(TemplateView):
    "herhangi kullanıcının anasayfası"
    template_name = "apps/cooggerapp/users/user.html"
    pagi = 6
    ctof = Content.objects.filter
    title = "{} | coogger"
    keywords = "{},{} {}"
    description = "{} {},{} adı ile coogger'da"

    def get_context_data(self, username, **kwargs):
        user = User.objects.filter(username = username)[0]
        try:
            OtherInformationOfUsers(user = user).save()
        except:
            pass
        queryset = self.ctof(user = user,status = "approved")
        info_of_cards = paginator(self.request,queryset,self.pagi)
        context = super(UserClassBased, self).get_context_data(**kwargs)
        nav_category = []
        for i in queryset:
            c_list = i.content_list
            if c_list not in nav_category:
                nav_category.append(c_list)
        context["content"] = info_of_cards
        context["content_user"] = User.objects.filter(username = username)[0]
        context["user_follow"] = users_web(user)
        context["nav_category"] = nav_category
        context["head"] = self.html_head(username,user)
        context["is_follow"] = is_follow(self.request,user)
        return context

    def html_head(self, username,user):
        html_head = dict(
         title = self.title.format(username),
         keywords = self.keywords.format(username,user.first_name,user.last_name),
         description = self.description.format(user.first_name,user.last_name,username),
         author = get_facebook(user),
        )


class UserTopic(UserClassBased): # TODO: görüntülenemiyor url adresinden dolayı hallet
    "kullanıcıların konu adresleri"
    keywords = "{} {},{}"
    description = "{} kullanıcımızın {} adlı içerik listesi"

    def get_context_data(self, utopic, username, **kwargs):
        context = super(UserTopic, self).get_context_data(username,**kwargs)
        user = context["content_user"]
        user_queryset = self.ctof(user = user)
        queryset = user_queryset.filter(content_list = utopic,status = "approved")
        info_of_cards = paginator(self.request,queryset,self.pagi)
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
    template_name = "apps/cooggerapp/users/user.html"
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
            c_list = i.content_list
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
        context["is_follow"] = is_follow(request,user)
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


class FollowBaseClass(View):
    oiouof = OtherInformationOfUsers.objects.filter

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            which_user = request.POST["which_user"]
            user = User.objects.filter(username = which_user)[0]
            request_user = request.user
            if user != request_user: # takip isteği ve kişisi aynı değil ise
                is_follow = Following.objects.filter(user = request_user,which_user = user)
                followers_num = self.oiouof(user = user)[0].follower_count
                if is_follow.exists():
                    is_follow.delete()
                    self.oiouof(user = request_user).update(following_count = F("following_count")-1)
                    self.oiouof(user = user).update(follower_count = F("follower_count")-1)
                    return HttpResponse(json.dumps({"ms":"Follow","num":followers_num-1}))
                Following(user = request_user,which_user = user).save()
                self.oiouof(user = request_user).update(following_count = F("following_count")+1)
                self.oiouof(user = user).update(follower_count = F("follower_count")+1)
                return HttpResponse(json.dumps({"ms":"Following","num":followers_num+1}))

def is_follow(request,user):
    try:
        is_follow = Following.objects.filter(user = request.user,which_user = user)
        if is_follow.exists():
            return "Following"
        return "Follow"
    except:
        pass
