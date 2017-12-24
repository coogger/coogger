from django.http import *
from django.shortcuts import render
from django.contrib.auth.models import User,Permission
from django.contrib.auth import *
from django.contrib import messages as ms
from cooggerapp.models import Author,OtherInformationOfUsers
from cooggerapp.forms import AuthorForm
from django.contrib.auth.models import User


def mysignup(request): #kayıt ol
    if request.method == "GET":
        if request.user.username:
            ms.error(request,"Yeni hesap açma işlemi için önce çıkış yapmalısınız")
            return HttpResponseRedirect("/")
        html_head = dict(
            title = "Kayıt ol | coogger",
            keywords = "Kayıt ol,coogger kayıt ol,coogger kaydol",
            description = "coogger'a kaydol"
        )
        context = dict(
            head = html_head,
        )
        template = "signup_or_login/sign.html"
        return render(request,template,context)
    elif request.method == "POST":
        if request.user.username:
            ms.error(request,"Yeni hesap açma işlemi için önce çıkış yapmalısınız")
            return HttpResponseRedirect("/")
        name = request.POST.get("Name")
        surname = request.POST.get("Surname")
        email=request.POST.get("Email")
        username=request.POST.get("Username")
        password=request.POST.get("Password")
        confirm=request.POST.get("Confirm")
        check = check_user(request,username,password,confirm)
        if not check:
            return HttpResponseRedirect("/signup")
        try:
            user = User.objects.create_user(first_name=name,last_name=surname,email = email,username=username,password=password)
        except:
            ms.error(request,"Bu kullanıcı ismi alınmış, farklı bir kullanıcı ismi ile kayıt olmayı deneyin")
            return HttpResponseRedirect("/signup")
        if user is not None:
            user.is_active=True
            user.save()
            user = authenticate(username=username, password=password)
            OtherInformationOfUsers(user = user,pp=False,is_author=False,author=False).save()
            login(request, user)
            ms.success(request,"Başarılı bir şekilde kayıt oldunuz {}".format(username))
            return HttpResponseRedirect("/")
        else:
            ms.success(request,"Kayıt sırasında beklenmedik hata {}".format(username))
            return HttpResponseRedirect("/")

def mylogin(request): # giriş yap
    username = request.user.username
    if request.method == "GET":
        if username:
            ms.error(request,"Başarıyla giriş yaptınız {}".format(username))
            return HttpResponseRedirect("/")
        html_head = dict(
            title = "coogger | Giriş yap",
            keywords = "coogger giriş yap",
            description = "coogger'a giriş yap"
        )
        context = dict(
            head = html_head,
        )
        template = "signup_or_login/login.html"
        return render(request,template,context)
    elif request.method == "POST":
        if username:
            ms.error(request,"ops {}".format(username))
            return HttpResponseRedirect("/")
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
    username = request.user.username
    if not username:
        ms.error(request,"ops !")
        return HttpResponseRedirect("/")
    try:
        logout(request)
    except KeyError:
        ms.error(request,"Çıkış yapılırken beklenmedik hata oluştur")
    ms.success(request,"Tekrar görüşmek üzere {}".format(username))
    return HttpResponseRedirect("/")

def signup_author(request):
    request_username = request.user.username
    otherinfo_form = AuthorForm(request.POST or None)
    if otherinfo_form.is_valid():
        if not request_username:
            ms.error(request,"ops !")
            return HttpResponseRedirect("/")
        otherinfo_form = otherinfo_form.save(commit=False)
        user_id = User.objects.filter(username = request_username)[0].id
        otherinfo_form.user_id = user_id
        otherinfo_form.pp = True
        otherinfo_form.is_author = False
        otherinfo_form.author = True
        otherinfo_form.save()
        OtherInformationOfUsers.objects.filter(user_id = user_id).update(author = True)
        ms.success(request,"Yazarlık başvurunuzu değerlendireceğiz bu genellikle 2-3 gün sürer {}".format(request_username))
        return HttpResponseRedirect("/")
    if not request_username:
        ms.error(request,"ops !")
        return HttpResponseRedirect("/")
    user_id = User.objects.filter(username = request_username)[0].id
    is_done_author = OtherInformationOfUsers.objects.filter(user_id = user_id)[0].author # yazarlık başvurusu yapmışmı
    if is_done_author:
        ms.error(request,"Yazarlık başvurunuzu daha önceden almıştık, değerlendirme süreci bitiminde sizinle iletişime geçeceğiz")
        return HttpResponseRedirect("/control")
    html_head = dict(
        title = "Yazarlık başvurusu | coogger",
        keywords = "coogger yazarlık,coogger yazarlık başvurusu",
        description = "coogger'a yazarlık başvurusu"
    )
    context = dict(
        signup_or_login = True,
        head = html_head,
        otherinfo_form = otherinfo_form,
    )
    template = "signup_or_login/signup-blogger.html"
    return render(request,template,context)

def check_user(request,username,password,confirm):
    if password != confirm:
        ms.error(request,"Şifreler eşleşmedi")
        return False
    elif len(password) < 4:
        ms.error(request,"Şifreniz en az 4 basamaklı olmalı")
        return False
    current_character = "qwertyuopilkjhgfdsazxcvbnm0123456789_"
    for i in username:
        if i in current_character:
            pass
        else:
            ms.error(request,"Kullanıcı isminizi belirlerken sadece {} karakterleri kullanmalısınız".format(current_character))
            return False
    return True # yani tüm şifre kurallarına uydu ise
