#django
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import F
from django.contrib import messages as ms
from django.utils.text import slugify
from django.utils import timezone

#models
from cooggerapp.models import Content,Contentviews,UserFollow,Comment,Notification

#views
from cooggerapp.views.tools import (get_ip,html_head,get_head_img_pp,content_cards,hmanynotifications,users_web)

#python
import json
import os
from bs4 import BeautifulSoup

def main_detail(request,username,utopic,path):
    "blogların detay kısmı "
    content_path = username+"/"+utopic+"/"+path
    ctof = Content.objects.filter
    queryset = ctof(url = content_path)[0]
    content_user = queryset.user
    ip = get_ip(request)
    if ip is not None: # ip adres almada bir sorun olursa
        if not Contentviews.objects.filter(content = queryset,ip = ip).exists():
            Contentviews(content = queryset,ip = ip).save()
            queryset.views = F("views") + 1
            queryset.save()
            # bundan dolayı okuma hemen 1 artmış olmaz
        # açılan makale bittikten sonra okunulan liste altındaki diğer paylaşımları anasayfadaki gibi listeler
    queryset = ctof(url = content_path)[0]
    content_id = queryset.id
    nav_category = ctof(user = content_user,content_list = utopic)
    info_of_cards = content_cards(request,nav_category,6)
    context = dict(
    head = html_head(queryset),
    content_user = content_user,
    nav_category = nav_category,
    nameoftopic = queryset.title,
    nameoflist = utopic,
    content = info_of_cards[0],
    detail = queryset,
    global_hashtag = [i for i in queryset.tag.split(",") if i != ""],
    comment_form = Comment.objects.filter(content=queryset),
    hmanynotifications = hmanynotifications(request),
    user_follow = users_web(content_user),
    )
    template = "detail/main_detail.html"
    return render(request,template,context)

def comment(request,content_path):
    if request.method=="POST" and request.is_ajax() and request.user.is_authenticated:
        user = request.user
        comment = request.POST["comment"]
        if comment != "":
            content = Content.objects.filter(url = content_path)[0]
            Comment(user=user,comment=comment,content = content).save()
            query = Content.objects.filter(url = content_path)[0]
            query.hmanycomment = F("hmanycomment")+1
            query.save()
            if str(content.user) != str(user.username):
                Notification(user=content.user,even = 1,content=comment,address = content_path).save()
            return HttpResponse(json.dumps({"comment": comment,"username":request.user.username,"img":get_head_img_pp(request.user)[0]}))
        return HttpResponse(None)
