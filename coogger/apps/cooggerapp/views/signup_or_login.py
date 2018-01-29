#django
from django.http import *
from django.shortcuts import render
from django.contrib.auth.models import User,Permission
from django.contrib.auth import *
from django.contrib import messages as ms
from django.contrib.auth.models import User

# class
from django.views.generic import ListView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

#models
from apps.cooggerapp.models import Author,OtherInformationOfUsers

#views
from apps.cooggerapp.views.tools import is_user_author

#forms
from apps.cooggerapp.forms import AuthorForm,UserForm


class MySignupBasedClass(View):
    form_class = UserForm
    template_name = "signup_or_login/sign.html"
    template_url = "/web/signup"
    title = "Kayıt ol | coogger"
    keywords = "Kayıt ol,coogger kayıt ol,coogger kaydol"
    description = "coogger'a kaydol"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            context = dict(
                signup_or_login = True,
                head = {"title":self.title,"keywords":self.keywords,"description":self.description},
                UserForm = self.form_class(),
            )
            return render(request,self.template_name,context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            sign_form = self.form_class(request.POST or None)
            if sign_form.is_valid():
                sign_form = sign_form.save(commit=False)
                username = sign_form.username
                if sign_form.password != request.POST["Confirm"]:
                    ms.error(request,"Şifreler eşleşmedi")
                    return HttpResponseRedirect(template_url)
                sign_form.save()
                user = User.objects.filter(username = username)[0]
                OtherInformationOfUsers(user = user).save()
                login(request, user)
                ms.success(request,"Başarılı bir şekilde kayıt oldunuz {}".format(username))
                return HttpResponseRedirect("/")
            return HttpResponse(self.get(request, *args, **kwargs))

class LoginBasedClass(View):
    template_name = "signup_or_login/login.html"
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
            username=request.POST["Username"]
            password=request.POST["Password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/")
            ms.warning(request,"Böyle bir kullanıcı bulunmamakta, lütfen şifrenizi ve kullanıcı adınızı kontrol ediniz")
            return HttpResponseRedirect(self.template_url)

class LogoutBasedClass(View):
    error = "Çıkış yapılırken beklenmedik hata oluştur"
    success = "Tekrar görüşmek üzere {}"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            ms.success(request,self.success.format(request.user.username))
            return HttpResponseRedirect("/")

class SingupAuthorBasedClass(View):
    form_class = AuthorForm
    template_name = "signup_or_login/signup-blogger.html"
    title = "Yazarlık başvurusu | coogger"
    keywords = "coogger yazarlık,coogger yazarlık başvurusu"
    description = "coogger'a yazarlık başvurusu"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        request_user = request.user
        try:
            instance_ = Author.objects.filter(user = request_user)[0]
            otherinfo_form = self.form_class(request.GET, instance = instance_)
        except AttributeError:
            otherinfo_form = self.form_class(request.GET)
        except IndexError:
            otherinfo_form = self.form_class(request.GET)
        is_done_author = OtherInformationOfUsers.objects.filter(user = request_user)[0].is_author
        if not is_done_author:
            context = dict(
                signup_or_login = True,
                head = {"title":self.title,"keywords":self.keywords,"description":self.description},
                otherinfo_form = otherinfo_form,
            )
            return render(request,self.template_name,context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        otherinfo_form = self.from_class(request.POST)
        if otherinfo_form.is_valid():
            otherinfo_form = otherinfo_form.save(commit=False)
            otherinfo_form.user = request_username
            otherinfo_form.save()
            ms.success(request,"Yazarlık başvurunuzu değerlendireceğiz bu genellikle 1-2 gün sürer {}".format(request_username))
            return HttpResponseRedirect("/")
