from django.http import *
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages as ms

def signup(request): #kayıt ol
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
        user = User.objects.create_user(username,0, password)
        user.is_active=True
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username']=username # buraya username yerine kanal linki oluşturup onu ver herkesin bir kanal linki olsun
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
            request.session['username']=username
            ms.success(request,"Hoşgeldin {}".format(username))
            return HttpResponseRedirect("/")
        ms.warning(request,"Böyle bir kullanıcı bulunmamakta, lütfen şifrenizi ve kullanıcı adınızı kontrol ediniz")
        return HttpResponseRedirect("/login")

def logout(request): # çıkış
    try:
        del request.session["username"]
        logout(request)
    except KeyError:
        ms.error(request,"Çıkış yapılırken beklenmedik hata oluştur")
    return HttpResponseRedirect("/")