# kullanıcıların yaptıkları tüm işlemler
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages as ms
from cooggerapp.models import *
from PIL import Image
import os

def user(request,username): 
    "herhangi kullanıcının anasayfası"
    pp = False
    if os.path.exists(os.getcwd()+"/coogger/media/users/pp/pp-"+username+".jpg"):
        pp = True
    content_list = ContentList.objects.all()
    output = dict(
        users = True,
        username = username,
        pp = pp,
        content_list = content_list,
    )
    return render (request,"users/user.html",output)

def upload_pp(request):
    "kullanıcılar profil resmini  değiştirmeleri için"
    username = request.user.username
    if request.method == "POST":
        try:
            image=request.FILES['u-upload-pp']
        except:
            ms.error(request,"Dosya alma sırasında bir sorun oluştu")
            return HttpResponseRedirect("/@"+username)

        with open(os.getcwd()+"/coogger/media/users/pp/pp-"+username+".jpg",'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        im = Image.open(os.getcwd()+"/coogger/media/users/pp/pp-"+username+".jpg")
        im.thumbnail((150,150))
        im.save(os.getcwd()+"/coogger/media/users/pp/pp-"+username+".jpg", "JPEG")
        return HttpResponseRedirect("/@"+username)

def u_topic(request):
    "kullanıcıların kendi hesaplarında açmış olduğu konulara yönlendirme"
    pass
