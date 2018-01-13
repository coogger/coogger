#django
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages as ms
from django.contrib.auth.models import User

#views
from cooggerapp.views.tools import hmanynotifications

#forms
from cooggerapp.forms import CSettingsUserForm,UserFollowForm

#python
import os

def profile(request):
    if not request.user.is_authenticated:
        return HttpResponse(None)
    user_form = CSettingsUserForm(request.POST or None,instance=request.user)
    if user_form.is_valid(): # post
        form = user_form.save(commit=False)
        if request.user.username != form.username:
            os.rename("/coogger/media/users/pp/pp-"+request.user.username+".jpg","/coogger/media/users/pp/pp-"+form.username+".jpg")
        form.save()
        return HttpResponseRedirect(request.META["PATH_INFO"])
    context = dict(
    CSettingsUserForm = user_form,
    settings = True,
    hmanynotifications = hmanynotifications(request),
    )
    template = "settings/profile.html"
    return render(request,template,context)

def account(request):
    if not request.user.is_authenticated:
        return HttpResponse(None)
    if request.method == "POST":
        password=request.POST.get("Password")
        confirm=request.POST.get("Confirm")
        if password == confirm:
             u = User.objects.get(username=request.user)
             u.set_password(password)
             u.save()
             ms.error(request,"Şifreniz başarıyla değişti, lütfen tekrar giriş yapınız")
             return HttpResponseRedirect("/login")
        else:
            ms.error(request,"Şifreler eşleşmedi")
            return HttpResponseRedirect("/settings/account")
    elif request.method == "GET":
        context = dict(
        settings = True,
        hmanynotifications = hmanynotifications(request),
        )
        template = "settings/account.html"
        return render(request,template,context)

def add_address(request):
    if not request.user.is_authenticated:
        return HttpResponse(None)
    user_form = UserFollowForm(request.POST or None)
    if user_form.is_valid(): # post
        form = user_form.save(commit=False)
        form.user = request.user
        form.save()
        ms.error(request,"Web siteniz eklendi")
        return HttpResponseRedirect(request.META["PATH_INFO"])
    context = dict(
    UserForm = user_form,
    settings = True,
    hmanynotifications = hmanynotifications(request),
    )
    template = "settings/add-address.html"
    return render(request,template,context)
