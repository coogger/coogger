from django.http import *
from django.shortcuts import render
from django.contrib.auth.models import User,Permission
from django.contrib.auth import *
from django.contrib import messages as ms
from cooggerapp.models import Author


def mysignup(request): #kayıt ol
    if request.method == "GET":
        if request.user.username:
            ms.error(request,"Yeni hesap açma işlemi için önce çıkış yapmalısınız")
            return HttpResponseRedirect("/")
        elastic_search = dict(
            title = "coogger | kayıt ol",
            keywords = "coogger,kayıt ol,coogger kayıt ol,kayıt,coogger kayıt,blog kayıt,blog yaz",
            description = "coogger a hoşgeldin ister normal üyeliği saçebilir ve yazarlarımızı takip edebilir istersende yazar olarak kayıt olabilir ve kazandığın paraları alabilirsin"
        )
        output = dict(
            signup_or_login = True,
            elastic_search = elastic_search
        )
        return render(request,"signup_or_login/sign.html",output)
    elif request.method == "POST":
        if request.user.username:
            ms.error(request,"Yeni hesap açma işlemi için önce çıkış yapmalısınız")
            return HttpResponseRedirect("/")
        name = request.POST.get("Name")
        surname = request.POST.get("Surname")
        email=request.POST.get("EmailorPhone")
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
        user.is_active=True
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            ms.success(request,"Başarılı bir şekilde kayıt oldunuz {}".format(username))
            return HttpResponseRedirect("/")

def mylogin(request): # giriş yap
    username = request.user.username
    if request.method == "GET":
        if username:
            ms.error(request,"Başarıyla giriş yaptınız {}".format(username))
            return HttpResponseRedirect("/")
        elastic_search = dict(
            title = "coogger | Giriş yap",
            keywords = "coogger,giriş yap,coogger giriş yap,giriş,login",
            description = "coogger a hoşgeldin açmış olduğun hesaba giriş yap"
        )
        output = dict(
            signup_or_login = True,
            elastic_search = elastic_search
        )
        return render(request,"signup_or_login/login.html",output)
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
    if request.is_ajax():
        if not request_username:
            ms.error(request,"ops !")
            return HttpResponseRedirect("/")
        return render(request,"signup_or_login/signup-blogger.html",{})
    elif request.method == "POST":
        if not request_username:
            ms.error(request,"ops !")
            return HttpResponseRedirect("/")
        phone=request.POST.get("Phone")
        iban = request.POST.get("Iban")
        username = request.POST.get("Username")
        password = request.POST.get("Password")
        
        if username != request_username:
            ms.success(request,"Kullanıcı adınızı yanlış yazdınız")
            return HttpResponseRedirect("/")
        user = authenticate(username=username, password=password)
        if user is None:
            ms.success(request,"Kullanıcı adınız ve şifreniz eşleşmedi")
            return HttpResponseRedirect("/")
        User.objects.filter(username = username).update(email = phone)   
        Author(user = user,iban=iban).save()
        ms.success(request,"Yazarlık başvurunuzu değerlendireceğiz bu genellikle 2-3 gün sürer {}".format(username))
        return HttpResponseRedirect("/")
    elif request.method == "GET":
        if not request_username:
            ms.error(request,"ops !")
            return HttpResponseRedirect("/")
        user_id = User.objects.filter(username = request_username)[0].id
        is_iban = Author.objects.filter(user_id = user_id)
        if is_iban.exists():
            ms.error(request,"Yazarlık başvurunuzu daha önceden almıştık, değerlendirme süreci bitiminde sizinle iletişime geçeceğiz")
            return HttpResponseRedirect("/control")
        elastic_search = dict(
            title = "coogger | kayıt ol",
            keywords = "coogger,kayıt ol,coogger kayıt ol,kayıt,coogger kayıt,blog kayıt,blog yaz",
            description = "coogger a hoşgeldin ister normal üyeliği saçebilir ve yazarlarımızı takip edebilir istersende yazar olarak kayıt olabilir ve kazandığın paraları alabilirsin"
        )
        output = dict(
            signup_or_login = True, 
            elastic_search = elastic_search
        )
        return render(request,"signup_or_login/signup-blogger.html",output)

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