#django
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages as ms
from django.contrib.auth.models import User

# class
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

#models
from cooggerapp.models import UserFollow

#views
from cooggerapp.views.tools import hmanynotifications,is_user_author

#forms
from cooggerapp.forms import CSettingsUserForm,UserFollowForm

#python
import os


class ProfileBasedClass(View):
    form_class = CSettingsUserForm
    template_name = "settings/profile.html"
    pp_path = "/coogger/media/users/pp/pp-{}.jpg"

    #@method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict(
        CSettingsUserForm = self.form_class(request.GET or None,instance=request.user),
        settings = True,
        hmanynotifications = hmanynotifications(request),
        )
        return render(request,self.template_name,context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        request_user = request.user
        user_form = self.form_class(request.POST,instance=request.user)
        if user_form.is_valid():
            form = user_form.save(commit=False)
            form_username = form.username
            if request_user.username != form_username:
                try:
                    os.rename(self.pp_path.format(request_user.username),self.pp_path.format(form_username))
                except FileNotFoundError:
                    pass
            form.save()
            return HttpResponseRedirect(request.META["PATH_INFO"])
        return HttpResponse(self.get(request, *args, **kwargs))

class AccountBasedClass(View):
    template_name = "settings/account.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = dict(
        settings = True,
        hmanynotifications = hmanynotifications(request),
        )
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            password=request.POST["Password"]
            if password == request.POST["Confirm"]:
                 u = User.objects.get(username=request.user)
                 u.set_password(password)
                 u.save()
                 ms.error(request,"Şifreniz başarıyla değişti, lütfen tekrar giriş yapınız")
                 return HttpResponseRedirect("/login")
            else:
                ms.error(request,"Şifreler eşleşmedi")
                return HttpResponseRedirect("/settings/account")

class AddaddessBasedClass(View):
    form_class = UserFollowForm
    model = UserFollow
    template_name = "settings/add-address.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        instance_ = self.model.objects.filter(user = request.user)
        user_form = self.form_class(request.GET)
        context = dict(
        UserForm = user_form,
        settings = True,
        instance_ = instance_,
        hmanynotifications = hmanynotifications(request),
        )
        return render(request,self.template_name,context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            user_form = self.form_class(request.POST)
            if user_form.is_valid():
                form = user_form.save(commit=False)
                form.user = request.user
                form.save()
                ms.error(request,"Web siteniz eklendi")
                return HttpResponseRedirect(request.META["PATH_INFO"])
            return HttpResponse(self.get(request, *args, **kwargs))
