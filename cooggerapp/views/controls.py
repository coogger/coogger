#django
from django.http import *
from django.shortcuts import render
from django.db.models import F
from django.utils.text import slugify
from django.contrib import messages as ms
from django.contrib.auth.models import User
from django.contrib.auth import *

#models
from cooggerapp.models import Content,ContentList

#views
from cooggerapp.views.tools import durationofread,hmanynotifications

#form
from cooggerapp.forms import ContentForm

#python
import random
import datetime

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
        content.dor = durationofread(content.content+title)
        content_tag = request.POST["tag"].split(",")
        tags = ""
        for i in content_tag:
            if i == content_tag[-1]:
                tags += slugify(i)
            else:
                tags += slugify(i)+","
        content.tag = tags
        url = slugify(title)
        try:
            content.url = request_user.username+"/"+content_list+"/"+url
            content.save()
        except:
            url = url+"-"+str(random.random()).replace(".","")[:6]
            content.url = request_user.username+"/"+content_list+"/"+url
            content.save()
        try:
            content_list_save = ContentList.objects.filter(user = request_user,content_list = content_list)[0]
            content_list_save.content_count = F("content_count")+1
            content_list_save.save()
            # kullanıcının açmış oldugu listeleri kayıt ediyoruz
        except: # önceden oluşmuş ise hata verir ve biz 1 olarak kayıt ederiz
            ContentList(user = request_user,content_list = content_list,content_count = 1).save()
        redirect = "/"+request_user.username+"/"+content_list+"/"+url
        return HttpResponseRedirect(redirect)
    # get method
    context = dict(
        controls = True,
        create_form = create_form,
        hmanynotifications = hmanynotifications(request),
    )
    template = "controls/create.html"
    return render(request,template,context)

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
        content.confirmation = False
        content.lastmod = datetime.datetime.now()
        title = content.title
        content.dor = durationofread(content.content+title)
        content_tag = request.POST["tag"].split(",")
        tags = ""
        for i in content_tag:
            if i == content_tag[-1]:
                tags += slugify(i)
            else:
                tags += slugify(i)+","
        content.tag = tags
        url = slugify(title)
        try:
            content.url = request_user.username+"/"+content_list+"/"+url
            content.save()
        except:
            url = url+"-"+str(random.random()).replace(".","")[:6]
            content.url = request_user.username+"/"+content_list+"/"+url
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
        return HttpResponseRedirect("/"+str(real_username)+"/"+content_list+"/"+url)
    # get method
    context = dict(
        controls = True,
        change = queryset,
        content_id = content_id,
        change_form = change_form,
    )
    template = "controls/change.html"
    return render(request,template,context)
