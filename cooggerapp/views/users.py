#django
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.contrib import messages as ms
from django.db.models import F

# class
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

#models
from cooggerapp.models import OtherInformationOfUsers,Content,UserFollow,Following

#forms
from cooggerapp.forms import UserFollowForm,AboutForm

#views
from cooggerapp.views.tools import hmanynotifications,get_facebook,users_web,paginator

#python
from PIL import Image
import os
import json

class UserBasedClass(TemplateView):
    "herhangi kullanıcının anasayfası"
    template_name = "users/user.html"
    pagi = 16
    ctof = Content.objects.filter
    title = "{} | coogger"
    keywords = "{},{} {}"
    description = "{} {},{} adı ile coogger'da"

    def get_context_data(self, username, **kwargs):
        user = User.objects.filter(username = username)[0]
        if username == self.request.user.username: # kendisi ise
            queryset = self.ctof(user = user)
        else:
            queryset = self.ctof(user = user,confirmation = True)
        info_of_cards = paginator(self.request,queryset,self.pagi)
        context = super(UserBasedClass, self).get_context_data(**kwargs)
        nav_category = []
        for i in queryset:
            c_list = i.content_list
            if c_list not in nav_category:
                nav_category.append(c_list)
        html_head = dict(
         title = self.title.format(username),
         keywords = self.keywords.format(username,user.first_name,user.last_name),
         description = self.description.format(user.first_name,user.last_name,username),
         author = get_facebook(user),
        )
        context["content"] = info_of_cards
        context["content_user"] = user
        context["user_follow"] = users_web(user)
        context["nav_category"] = nav_category
        context["head"] = html_head
        context["hmanynotifications"] = hmanynotifications(self.request)
        context["is_follow"] = is_follow(self.request,user)
        return context


class UserTopicBasedClass(UserBasedClass):
    "kullanıcıların konu adresleri"
    keywords = "{} {},{}"
    description = "{} kullanıcımızın {} adlı içerik listesi"

    def get_context_data(self, username, utopic, **kwargs):
        context = super(UserTopicBasedClass, self).get_context_data(username,**kwargs)
        user = context["content_user"]
        user_queryset = self.ctof(user = user)
        if username == self.request.user.username:
            queryset = user_queryset.filter(content_list = utopic)
        else:
            queryset = user_queryset.filter(content_list = utopic,confirmation = True)
        html_head = dict(
         title = self.title.format(username+" - "+utopic),
         keywords = self.keywords.format(username,utopic,utopic),
         description = self.description.format(username,utopic),
         author = get_facebook(user),
        )
        context["user_follow"] = users_web(user)
        context["head"] = html_head
        context["nameoftopic"] = utopic
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
        queryset = Content.objects.filter(user = user,confirmation = True)
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
        context["nav_category"] = [i.content_list for i in queryset]
        context["head"] = html_head
        context["hmanynotifications"] = hmanynotifications(request)
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
                    about_form.save()
                return HttpResponse(self.get(request, username, *args, **kwargs))


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
                followers_num = self.oiouof(user = user)[0].followers
                if is_follow.exists():
                    is_follow.delete()
                    self.oiouof(user = request_user).update(following = F("following")-1)
                    self.oiouof(user = user).update(followers = F("followers")-1)
                    return HttpResponse(json.dumps({"ms":"Takip et","num":followers_num-1}))
                Following(user = request_user,which_user = user).save()
                self.oiouof(user = request_user).update(following = F("following")+1)
                self.oiouof(user = user).update(followers = F("followers")+1)
                return HttpResponse(json.dumps({"ms":"Takibi bırak","num":followers_num+1}))


class UploadppBasedClass(View):
    "kullanıcılar profil resmini  değiştirmeleri için"
    oiouof = OtherInformationOfUsers.objects.filter
    pp_path = os.getcwd()+"/coogger/media/users/pp/pp-{}.jpg"
    im_size = (350,350)
    error = "Resim dosyanız alınamadı, güncelle düymesine basarak resmi seçiniz"

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.pp_path = self.pp_path.format(request_user.username)
        request_user = request.user
        image=request.FILES['u-upload-pp']
        with open(self.pp_path,'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        im = Image.open(self.pp_path)
        im.thumbnail(im_size)
        im.save(self.pp_path, "JPEG")
        self.oiouof(user = request_user).update(pp = True)
        return HttpResponseRedirect("/"+request_user.username)

def is_follow(request,user):
    try:
        is_follow = Following.objects.filter(user = request.user,which_user = user)
        if is_follow.exists():
            return "Takibi bırak"
        return "Takip et"
    except:
        pass
