#django
from django.http import *
from django.shortcuts import render
from django.contrib import messages as ms
from django.contrib.auth import logout
from django.contrib.auth.models import User,Permission
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# class
#from django.views.generic import ListView
from django.views import View
from django.utils.decorators import method_decorator

#models
from apps.cooggerapp.models import OtherInformationOfUsers

#forms
from apps.cooggerapp.forms import UserSingupForm

class Login(View):
    template_name = "apps/cooggerapp/signup_or_login/login.html"
    template_url = "accounts/login/"
    title = "coogger | Giriş yap"
    keywords = "coogger giriş yap"
    description = "coogger'a giriş yap"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            context = dict(
                signup_or_login = True,
                head = dict(title = self.title,keywords = self.keywords,description = self.description),
            )
            return render(request,self.template_name,context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            username = request.POST["Username"]
            posting_key = request.POST["Postingkey"]
            user = authenticate(username = username, password = posting_key)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                user = User.objects.create_user(username = username, password = posting_key)
                user = User.objects.filter(username = username)[0]
                OtherInformationOfUsers(user = user, posting_key = posting_key).save()
                ms.success(request,"Başarılı bir şekilde kayıt oldunuz {}".format(username))
                login(request, user)
                return HttpResponseRedirect("/")
            ms.warning(request,"Böyle bir kullanıcı bulunmamakta, lütfen posting key'inizi ve kullanıcı adınızı kontrol ediniz")
            return HttpResponseRedirect(self.template_url)

class Logout(View):
    error = "Çıkış yapılırken beklenmedik hata oluştur"
    success = "Tekrar görüşmek üzere {}"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            ms.success(request,self.success.format(request.user.username))
            return HttpResponseRedirect("/")
