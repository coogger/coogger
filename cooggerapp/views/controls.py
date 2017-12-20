# content control
import random

from django.http import *
from django.shortcuts import render
from django.db.models import F
from django.utils.text import slugify

from django.contrib import messages as ms
from django.contrib.auth.models import User
from django.contrib.auth import *

from cooggerapp.forms import ContentForm
from cooggerapp.models import Content,ContentList
from cooggerapp.views import tools

def create(request):
    "to create new content"
    request_user = request.user
    if not request_user.is_authenticated or not request_user.otherinformationofusers.is_author:
        ms.error(request,"Bu sayfa için yetkili değilsiniz,lütfen Yazarlık başvurusu yapın")
        return HttpResponseRedirect("/")
    create_form = ContentForm(request.POST or None)
    # post method
    if create_form.is_valid():
        content = create_form.save(commit=False)
        content.user = request_user
        content_list = slugify(request.POST["content_list"])
        if content_list == "":
            content_list = "coogger"
        content.content_list = content_list
        title = content.title
        url = slugify(title)
        content.dor = tools.durationofread(content.content+title)
        content_tag = content.tag.split(",")
        tags = ""
        for i in content_tag:
            if i == content_tag[-1]:
                tags += slugify(i)
            else:
                tags += slugify(i)+","
        content.tag = tags
        try:
            content.url = "@"+request_user.username+"/"+content_list+"/"+url
            content.save()
        except:
            content.url = "@"+request_user.username+"/"+content_list+"/"+url+"-"+str(random.random()).replace(".","")
            content.save()
        try:
            content_list_save = ContentList.objects.filter(user = request_user,content_list = content_list)[0]
            content_list_save.content_count = F("content_count")+1
            content_list_save.save()
            # kullanıcının açmış oldugu listeleri kayıt ediyoruz
        except: # önceden oluşmuş ise hata verir ve biz 1 olarak kayıt ederiz
            ContentList(user = request_user,content_list = content_list,content_count = 1).save()

        return HttpResponseRedirect("/@"+request_user.username+"/"+content_list+"/"+url)
    # get method
    output = dict(
        controls = True,
        hmanynotifications = tools.hmanynotifications(request),
    )
    return render(request,"controls/create.html",output)

def change(request,content_id):
    "to change the content"
    request_user = request.user
    if not request_user.is_authenticated or not request_user.otherinformationofusers.is_author:
        ms.error(request,"Bu sayfa için yetkili değilsiniz,lütfen Yazarlık başvurusu yapın !")
        return HttpResponseRedirect("/")
    elif request_user.is_superuser:
        queryset = Content.objects.filter(id = content_id)
    else:
        queryset = Content.objects.filter(user = request_user,id = content_id)
    if not queryset.exists():
        ms.error(request,"Girmek istediğiniz sayfada yönetim iznine sahip değilsiniz !")
        return HttpResponseRedirect("/")
    queryset = queryset[0]
    real_username = queryset.user # içeriği yazan kişinin kullanıcı ismi
    old_content_list = str(queryset.content_list)
    change_form = ContentForm(request.POST or None,instance=queryset)
    # post method
    if change_form.is_valid():
        content = change_form.save(commit=False)
        content.user = real_username
        content_list = str(slugify(request.POST["content_list"]))
        content.content_list = content_list
        content.time = queryset.time
        title = content.title
        url = slugify(title)
        content.url = "@"+str(real_username)+"/"+content_list+"/"+url
        content.dor = tools.durationofread(content.content+title)
        content_tag = content.tag.split(",")
        tags = ""
        for i in content_tag:
            if i == content_tag[-1]:
                tags += slugify(i)
            else:
                tags += slugify(i)+","
        content.tag = tags
        content.save()
        if content_list != old_content_list: # content_list değişmiş ise
            real_user = User.objects.filter(username = real_username)[0]
            try:
                content_list_save = ContentList.objects.filter(user = real_user,content_list = old_content_list)[0]
                content_list_save.content_count = F("content_count")-1 # eskisini bir azaltıyor
                content_list_save.save()
                try:
                    ContentList.objects.filter(content_count = 0)[0].delete() # sıfır olanı siliyor
                except IndexError:
                    pass
            except IndexError:
                pass
            try:
                content_list_ = ContentList.objects.filter(user = real_user,content_list = content_list)[0]
                content_list_.content_count = F("content_count")+1
                content_list_.save()
            except:
                ContentList(user = real_user,content_list = content_list,content_count = 1).save()
        return HttpResponseRedirect("/@"+str(real_username)+"/"+content_list+"/"+url)
    # get method
    output = dict(
        controls = True,
        change = queryset,
        content_id = content_id,
        change_form = change_form,
    )
    return render(request,"controls/change.html",output)

def delete(request,content_id):
    "to delete the content"
    request_user = request.user
    if not request.is_ajax() or not request_user.username:
        ms.error(request,"ops !")
        return HttpResponseRedirect("/")
    elif request_user.is_superuser: # admin
        queryset = Content.objects.filter(id = content_id)
    else:
        queryset = Content.objects.filter(user = request_user,id = content_id)
    real_username = queryset[0].username # içeriği yazan kişinin kullanıcı ismi
    user = User.objects.filter(username = real_username)[0]
    if not queryset.exists():
        ms.error(request,"Girmek istediğiniz sayfada yönetim iznine sahip değilsiniz !")
        return HttpResponseRedirect("/")
    content_list = queryset[0].content_list
    try:
        queryset.delete()
        try:
            content_list_save = ContentList.objects.filter(user = user,content_list = content_list)[0]
            content_list_save.content_count = F("content_count")-1
            content_list_save.save()
            try:
                ContentList.objects.filter(content_count = 0)[0].delete()
            except:
                return HttpResponse("12312")
        except:
            return HttpResponse("Nesne silindi fakat nesneye ait liste silinemedi ")
    except:
        return HttpResponse("Silme işlemi sırasında beklenmedik hata !")
    return HttpResponse("Silme işlemi başarılı ")
