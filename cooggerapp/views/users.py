#django
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.contrib import messages as ms

#models
from cooggerapp.models import ContentList,OtherInformationOfUsers,Content,UserFollow

#forms
from cooggerapp.forms import UserFollowForm

#views
from cooggerapp.views.tools import hmanynotifications,get_facebook,users_web,content_cards

#python
from PIL import Image
import os

def user(request,username):
    "herhangi kullanıcının anasayfası"
    try:
        user = User.objects.filter(username = username)[0]
    except IndexError:
        ms.error(request,"{} adı ile bir kullanıcımız yoktur !".format(username))
        return HttpResponseRedirect("/")
    queryset = Content.objects.filter(user = user)
    info_of_cards = content_cards(request,queryset)
    html_head = dict(
     title = username+" | coogger",
     keywords =username+","+user.first_name+" "+user.last_name,
     description =user.first_name+" "+user.last_name+", "+username+" adı ile coogger'da",
     author = get_facebook(user),
    )
    context = dict(
        content = info_of_cards[0],
        content_user = user,
        paginator = info_of_cards[1],
        user_follow = users_web(user),
        nav_category = ContentList.objects.filter(user = user),
        head = html_head,
        hmanynotifications = hmanynotifications(request),
    )
    template = "users/user.html"
    return render(request,template,context)

def upload_pp(request):
    "kullanıcılar profil resmini  değiştirmeleri için"
    request_username = request.user.username
    if request.method == "POST":
        try:
            image=request.FILES['u-upload-pp']
        except:
            ms.error(request,"Dosya alma sırasında bir sorun oluştu")
            return HttpResponseRedirect("/@"+request_username)
        with open(os.getcwd()+"/coogger/media/users/pp/pp-"+request_username+".jpg",'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        im = Image.open(os.getcwd()+"/coogger/media/users/pp/pp-"+request_username+".jpg")
        im.thumbnail((350,350))
        try: # resim yükleme sırasında bir hata olursa pp = False olacak hata olmaz ise True
            im.save(os.getcwd()+"/coogger/media/users/pp/pp-"+request_username+".jpg", "JPEG")
            user_id = User.objects.filter(username = request_username)[0].id
            OtherInformationOfUsers.objects.filter(user_id = user_id).update(pp = True)
        except:
            OtherInformationOfUsers.objects.filter(user_id = user_id).update(pp = False)
        return HttpResponseRedirect("/@"+request_username)

def u_topic(request,username,utopic):
    "kullanıcıların kendi hesaplarında açmış olduğu konulara yönlendirme"
    user = User.objects.filter(username = username)[0]
    queryset = Content.objects.filter(user = user,content_list = utopic)
    if not queryset.exists():
        ms.error(request,"{} adlı kullanıcı nın {} adlı bir içerik listesi yoktur".format(username,utopic))
        return HttpResponseRedirect("/")
    info_of_cards = content_cards(request,queryset)
    nav_category = ContentList.objects.filter(user = user)
    html_head = dict(
     title = username+" - "+utopic+" | coogger",
     keywords = username+" "+utopic+","+utopic,
     description = username+" kullanıcımızın "+utopic+" adlı içerik listesi",
     author = get_facebook(user),
    )
    context = dict(
        content = info_of_cards[0],
        content_user = user,
        paginator = info_of_cards[1],
        nav_category = nav_category,
        nameoftopic = utopic,
        nameoflist = "Listeler",
        head = html_head,
        hmanynotifications = hmanynotifications(request),
        user_follow = users_web(user),
    )
    template = "users/user.html"
    return render(request,template,context)
