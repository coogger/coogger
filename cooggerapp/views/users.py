#django
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.contrib import messages as ms
from django.db.models import F

#models
from cooggerapp.models import ContentList,OtherInformationOfUsers,Content,UserFollow,Following

#forms
from cooggerapp.forms import UserFollowForm,AboutForm

#views
from cooggerapp.views.tools import hmanynotifications,get_facebook,users_web,content_cards

#python
from PIL import Image
import os
import json

def user(request,username):
    "herhangi kullanıcının anasayfası"
    try:
        user = User.objects.filter(username = username)[0]
    except IndexError:
        ms.error(request,"{} adı ile bir kullanıcımız yoktur !".format(username))
        return HttpResponseRedirect("/")
    if username == user:
        queryset = Content.objects.filter(user = user)
    else:
        queryset = Content.objects.filter(user = user,confirmation = True)
    info_of_cards = content_cards(request,queryset,16)
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
        is_follow = is_follow(request,user)
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
            return HttpResponseRedirect("/"+request_username)
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
        return HttpResponseRedirect("/"+request_username)

def u_topic(request,username,utopic):
    "kullanıcıların kendi hesaplarında açmış olduğu konulara yönlendirme"
    user = User.objects.filter(username = username)[0]
    if username == user:
        queryset = Content.objects.filter(user = user,content_list = utopic)
    else:
        queryset = Content.objects.filter(user = user,content_list = utopic,confirmation = True)
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

def about(request,username):
    try:
        user = User.objects.filter(username = username)[0]
    except IndexError:
        ms.error(request,"{} adı ile bir kullanıcımız yoktur !".format(username))
        return HttpResponseRedirect("/")
    query = OtherInformationOfUsers.objects.filter(user = user)[0]
    if request.user == user: # hesaba giren kendisi ise
        about  = AboutForm(request.POST or None,instance=query)
        if about.is_valid(): # ve post isteği ise
            about_ = about.save(commit = False)
            about_.user = user
            about_.save()
    else:#başkası ise
        about = query.about
    html_head = dict(
     title = username+" hakkımda | coogger",
     keywords = username+","+username+" hakkımda"+username+"hakkında",
     description = username + " kimdir ?",
     author = get_facebook(user),
    )
    context = dict(
        about = about,
        true_about = True,
        content_user = user,
        user_follow = users_web(user),
        nav_category = ContentList.objects.filter(user = user),
        head = html_head,
        hmanynotifications = hmanynotifications(request),
        is_follow = is_follow(request,user),
    )
    template = "users/user.html"
    return render(request,template,context)

def following(request):# TODO: bunu bir düzenle allah için
    if request.method=="POST" and request.is_ajax() and request.user.is_authenticated:
        which_user = request.POST["which_user"]
        user = User.objects.filter(username = which_user)[0]
        if user == request.user:
            return HttpResponse(None)
        is_follow = Following.objects.filter(user = request.user,which_user = user)
        num = OtherInformationOfUsers.objects.filter(user = user)[0]
        num2 = OtherInformationOfUsers.objects.filter(user = request.user)[0]
        num_ = num.followers
        if is_follow.exists():
            is_follow.delete()
            num2.following = F("following")-1
            num2.save()
            num.followers = F("followers")-1
            num.save()
            return HttpResponse(json.dumps({"ms":"Takip et","num":num_-1}))
        Following(user = request.user,which_user = user).save()
        num2.following = F("following")+1
        num2.save()
        num.followers = F("followers")+1
        num.save()
        return HttpResponse(json.dumps({"ms":"Takibi bırak","num":num_+1}))
    return HttpResponse(None)

def is_follow(request,user):
    try:
        is_follow = Following.objects.filter(user = request.user,which_user = user)
        if is_follow.exists():
            return "Takibi bırak"
        return "Takip et"
    except:
        return HttpResponse(None)
