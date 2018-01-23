#django
from django.http import HttpResponse
from django.contrib import messages as ms
from django.contrib.auth.models import User
from django.db.models import F

#models
from cooggerapp.models import UserFollow,Content,OtherInformationOfUsers

#python
import json

def address(request):
    if request.method=="POST" and request.is_ajax() and request.user.is_authenticated:
        address_id = int(request.POST["address_id"])
        ubf = UserFollow.objects.filter(id = address_id)[0]
        if ubf.user == request.user:
            ubf.delete()
        return HttpResponse(json.dumps({"status":"adres silindi"}))

def content(request,content_id):
    request_user = request.user
    if not request.is_ajax() or not request_user.username:
        ms.error(request,"ops !")
        return HttpResponseRedirect("/")
    elif request_user.is_superuser: # admin
        queryset = Content.objects.filter(id = content_id)
    else:
        queryset = Content.objects.filter(user = request_user,id = content_id)
    real_username = queryset[0].user # içeriği yazan kişinin kullanıcı ismi
    user = User.objects.filter(username = real_username)[0]
    if not queryset.exists():
        ms.error(request,"Girmek istediğiniz sayfada yönetim iznine sahip değilsiniz !")
        return HttpResponseRedirect("/")
    content_list = queryset[0].content_list
    queryset.delete()
    OtherInformationOfUsers.objects.filter(user = user).update(hmanycontent = F("hmanycontent") -1)
    return HttpResponse("Silme işlemi başarılı ")
