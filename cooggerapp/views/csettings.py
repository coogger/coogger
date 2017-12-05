from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages
from cooggerapp.views.tools import Topics,hmanynotifications
from django.contrib import messages as ms
from django.contrib.auth.models import User
from cooggerapp.forms import UserForm,UserFollowForm,UserFollowForm
import os

def profile(request):
    if not request.user.is_authenticated:
        return HttpResponse(None)
    template = "settings/profile.html"
    user_form = UserForm(request.POST or None,instance=request.user)
    if user_form.is_valid(): # post
        form = user_form.save(commit=False)
        if request.user.username != form.username:
            os.rename("/coogger/media/users/pp/pp-"+request.user.username+".jpg","/coogger/media/users/pp/pp-"+form.username+".jpg")
        form.save()
        return HttpResponseRedirect("/settings/")
    tools_topic = Topics()
    category = tools_topic.category
    output = dict(
        UserForm = user_form,
        settings = True,
        nav_category = category,
        hmanynotifications = hmanynotifications(request),
        )
    return render(request,template,output)

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
        template = "settings/account.html"
        tools_topic = Topics()
        category = tools_topic.category
        output = dict(
            settings = True,
            nav_category = category,
            hmanynotifications = hmanynotifications(request),
            )
        return render(request,template,output)

def add_address(request):
    if not request.user.is_authenticated:
        return HttpResponse(None)
    template = "settings/add-address.html"
    user_form = UserFollowForm(request.POST or None)
    if user_form.is_valid(): # post
        form = user_form.save(commit=False)
        form.user = request.user
        form.save()
        ms.error(request,"Web siteniz eklendi")
        return HttpResponseRedirect("/settings/add-address")
    tools_topic = Topics()
    category = tools_topic.category
    output = dict(
        UserForm = user_form,
        settings = True,
        nav_category = category,
        hmanynotifications = hmanynotifications(request),
        )
    return render(request,template,output)
