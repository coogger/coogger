#django
from django.http import *
from django.shortcuts import render
from django.db.models import F
from django.utils.text import slugify
from django.contrib import messages as ms
from django.contrib.auth.models import User
from django.contrib.auth import *

#models
from cooggerapp.models import Content,OtherInformationOfUsers

#views
from cooggerapp.views.tools import hmanynotifications

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
    content_form = ContentForm(request.POST or None)
    # post method
    if content_form.is_valid():
        content_form = content_form.save(commit=False)
        content_form.user = request_user
        content_form.confirmation = True
        OtherInformationOfUsers.objects.filter(user = request_user).update(hmanycontent = F("hmanycontent") + 1)
        content_form.save() # hiç hata olmaz ise kayıt etsindiye en sonda
        return HttpResponseRedirect("/"+content_form.url)
    # get method
    context = dict(
        create_form = content_form,
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
        ms.error(request,"Böyle bir sayfa yoktur.")
        return HttpResponseRedirect("/")
    queryset = queryset[0]
    old_content_list = queryset.content_list
    content_form = ContentForm(request.POST or None,instance=queryset)
    # post method
    if content_form.is_valid():
        content = content_form.save(commit=False)
        real_user = queryset.user # içeriği yazan kişinin kullanıcı ismi
        content.user = real_user
        content.time = queryset.time
        content.confirmation = True
        content.lastmod = datetime.datetime.now()     
        content.save()
        return HttpResponseRedirect("/"+content.url)
    # get method
    context = dict(
        change = queryset,
        content_id = content_id,
        change_form = content_form,
    )
    template = "controls/change.html"
    return render(request,template,context)
