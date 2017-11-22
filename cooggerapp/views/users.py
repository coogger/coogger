# kullanıcıların yaptıkları tüm işlemler
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.contrib import messages as ms
from cooggerapp.models import ContentList,OtherInformationOfUsers,Blog,UserFollow
from cooggerapp.forms import UserFollowForm
from cooggerapp.views import tools
from cooggerapp.views.home import content_cards
from PIL import Image
import os

def user(request,username):
    "herhangi kullanıcının anasayfası"
    user = User.objects.filter(username = username)[0]
    content_list = ContentList.objects.filter(user = user)
    try:
        user_follow = UserFollow.objects.filter(user = user)
    except:
        user_follow = []
    # yaptığı paylaşımlar
    queryset = Blog.objects.filter(username = user)
    info_of_cards = content_cards(request,queryset)
    try:
        img_pp = tools.get_head_img_pp(user)
    except:
        img_pp = ["/static/media/profil.png",None]
    facebook = get_facebook(user)
    elastic_search = dict(
     title = username+" | coogger",
     keywords =username+","+user.first_name+" "+user.last_name,
     description =user.first_name+" "+user.last_name+", "+username+" adı ile coogger'da",
     author = facebook,
     img = img_pp[0],
    )
    output = dict(
        users = True,
        pp = img_pp[1],
        img = img_pp[0],
        blog = info_of_cards[0],
        username = username,
        paginator = info_of_cards[1],
        user_follow = user_follow,
        content_list = content_list,
        ogurl = request.META["PATH_INFO"],
        elastic_search = elastic_search,
    )
    return render (request,"users/user.html",output)

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
        im.thumbnail((250,250))
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
    queryset = Blog.objects.filter(username = user,content_list = utopic)
    if not queryset.exists():
        ms.error(request,"{} adlı kullanıcı nın {} adlı bir içerik listesi yoktur".format(username,utopic))
        return HttpResponseRedirect("/")
    info_of_cards = content_cards(request,queryset)
    nav_category = [nav for nav in get_nav_category(user)]
    try:
        img_pp = tools.get_head_img_pp(request.user)
    except:
        img_pp = ["/static/media/profil.png",None]
    facebook = get_facebook(user)
    elastic_search = dict(
     title = username+" - "+utopic+" | coogger",
     keywords = username+" "+utopic+","+utopic,
     description = username+" kullanıcımızın "+utopic+" adlı içerik listesi",
     author = facebook,
     img = img_pp[0],
    )
    output = dict(
        blog = info_of_cards[0],
        pp = img_pp[0],
        img = img_pp[0],
        general = True,
        paginator = info_of_cards[1],
        username = username,
        nav_category = nav_category,
        ogurl = request.META["PATH_INFO"],
        nameoftopic = utopic,
        nameoflist = "Listeler",
        elastic_search = elastic_search,
    )
    return render(request,"blog/blogs.html",output)

def get_nav_category(user):
    top = tools.Topics()
    another_utopic = ContentList.objects.filter(user = user)
    for a_utopic in another_utopic:
        fuck = a_utopic.content_list
        yield fuck,fuck


def get_facebook(user):
    facebook = None
    try:
        for f in UserFollow.objects.filter(user = user):
            if f.choices  == "facebook":
                facebook = f.adress
    except:
        pass
    return facebook
