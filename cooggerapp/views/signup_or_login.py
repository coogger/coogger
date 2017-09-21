from django.http import *
from django.shortcuts import render
from django.contrib.auth.models import User,Permission
from django.contrib.auth import *
from django.contrib import messages as ms
from cooggerapp.models import Author


def mysignup(request): #kayıt ol
    if request.method == "GET":
        output = dict(
            signup_or_login = True
        )
        return render(request,"signup_or_login/sign.html",output)
    elif request.method == "POST":
        username=request.POST.get("Username")
        password=request.POST.get("Password")
        confirm=request.POST.get("Confirm")
        if password != confirm:
            ms.error(request,"Şifreler eşleşmedi")
            return HttpResponseRedirect("/signup")
        current_character = "qwertyuopilkjhgfdsazxcvbnm0123456789_"
        for i in username:
            if i in current_character:
                pass
            else:
                ms.error(request,"Kullanıcı isminizi belirlerken sadece {} karakterleri kullanmalısınız".format(current_character))
                return HttpResponseRedirect("/signup")
        user = User.objects.create_user(username,0, password)
        user.is_active=True
        user.is_staff=True
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            ms.success(request,"Başarılı bir şekilde kayıt oldunuz {}".format(username))
            return HttpResponseRedirect("/")

def mylogin(request): # giriş yap
    if request.method == "GET":
        output = dict(
            signup_or_login = True
        )
        return render(request,"signup_or_login/login.html",output)
    elif request.method == "POST":
        username=request.POST.get("Username")
        password=request.POST.get("Password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            ms.success(request,"Hoşgeldin {}".format(username))
            return HttpResponseRedirect("/")
        ms.warning(request,"Böyle bir kullanıcı bulunmamakta, lütfen şifrenizi ve kullanıcı adınızı kontrol ediniz")
        return HttpResponseRedirect("/login")

def mylogout(request): # çıkış
    try:
        logout(request)
    except KeyError:
        ms.error(request,"Çıkış yapılırken beklenmedik hata oluştur")
    return HttpResponseRedirect("/")

def signup_author(request):
    if request.is_ajax():
        return render(request,"signup_or_login/signup-blogger.html",{})
    elif request.method == "POST":
        name = request.POST.get("Name")
        surname = request.POST.get("Surname")
        iban = request.POST.get("Iban")
        username = request.POST.get("Username")
        password = request.POST.get("Password")
        confirm = request.POST.get("Confirm")
        if password != confirm:
            ms.error(request,"Şifreler eşleşmedi")
            return HttpResponseRedirect("/signup-author")
        current_character = "qwertyuopilkjhgfdsazxcvbnm0123456789_"
        for i in username:
            if i in current_character:
                pass
            else:
                ms.error(request,"Kullanıcı isminizi belirlerken sadece {} karakterleri kullanmalısınız".format(current_character))
                return HttpResponseRedirect("/signup-author") 
        user = User.objects.create_user(first_name=name,last_name=surname,username=username,password=password)
        user.is_active=True
        user.is_staff=True
        per = Permission.objects.get(name='Can add blog')
        user.user_permissions.add(per)
        user.save()
        Author(user =user,iban=iban).save()

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            ms.success(request,"Başarılı bir şekilde kayıt oldunuz {}".format(username))
            return HttpResponseRedirect("/")
    elif request.method == "GET":
        return render(request,"signup_or_login/signup-blogger.html",{"signup_or_login":True})