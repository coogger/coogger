# kullanıcıların yaptıkları tüm işlemler
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.contrib import messages as ms
from cooggerapp.models import *
from cooggerapp.views import tools
from PIL import Image
import os

def user(request,username): 
    "herhangi kullanıcının anasayfası"
    content_list = ContentList.objects.filter(username = username)
    user = User.objects.filter(username = username)
    pp = OtherInformationOfUsers.objects.filter(user = user)[0].pp
    user_info = user[0]
    elastic_search = dict(
     title = username+" | coogger",
     keywords =username+","+user_info.first_name+" "+user_info.last_name,
     description =user_info.first_name+", "+user_info.last_name+", "+username+" adı ile coogger'da",
    )

    output = dict(
        users = True,
        pp = pp,
        username = username,
        content_list = content_list,
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

        with open(os.getcwd()+"/media/users/pp/pp-"+request_username+".jpg",'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        im = Image.open(os.getcwd()+"/media/users/pp/pp-"+request_username+".jpg")
        im.thumbnail((150,150))
        im.save(os.getcwd()+"/media/users/pp/pp-"+request_username+".jpg", "JPEG")
        user_id = User.objects.filter(username = request_username)[0].id
        OtherInformationOfUsers.objects.filter(user_id = user_id).update(pp = True)
        return HttpResponseRedirect("/@"+request_username)

def u_topic(request,username,utopic):
    "kullanıcıların kendi hesaplarında açmış olduğu konulara yönlendirme"
    username = username.replace("/"+utopic,"")
    queryset = Blog.objects.filter(username = username,content_list = utopic)
    if not queryset.exists():
        ms.error(request,"{} adlı kullanıcı nın {} adlı bir yazı listesi yoktur".format(username,utopic))
        return HttpResponseRedirect("/")
    blogs = tools.paginator(request,queryset)
    paginator = blogs
    pp = tools.get_pp(blogs)
    stars = []
    for i in blogs:
        try:
            stars.append(str(int(i.stars/i.hmstars)+1))
        except ZeroDivisionError:
            stars.append("0")
    blogs = zip(blogs,pp,stars)
    top = tools.Topics()
    category = top.category
    subcategory = top.subcatecory
    category2 = top.category2
    elastic_search = dict(
     title = username+" - "+utopic+" | coogger",
     keywords = username+" "+utopic+","+utopic+",coogger "+utopic+","+utopic+","+username,
     description = username+" adlı kullanıcının "+utopic+" adlı içerik listesi",
    )
    output = dict(
        blog = blogs,
        topics_category = category,
        general = True,
        paginator = paginator,
        topics_another = subcategory+category2,
        username = username,
        elastic_search = elastic_search,
    )
    return render(request,"blog/blogs.html",output)
