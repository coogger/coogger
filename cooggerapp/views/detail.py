import json
import os
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import F
from django.utils.text import slugify
from django.utils import timezone
from bs4 import BeautifulSoup
from cooggerapp.models import Content,Contentviews,UserFollow,Comment,Notification
from cooggerapp.views.tools import (get_ip,html_head,get_head_img_pp,content_cards,hmanynotifications,users_web)


def main_detail(request,blog_path,utopic,path):
    "blogların detay kısmı "
    ctof = Content.objects.filter
    queryset = ctof(url = blog_path)[0]
    queryset2 = queryset # değişeceği için kopyalıyorum
    content_user = queryset.user
    ip = get_ip(request)
    if ip is not None: # ip adres almada bir sorun olursa
        if not Contentviews.objects.filter(content = queryset2,ip = ip).exists():
            Contentviews(content = queryset2,ip = ip).save()
            queryset2.views = F("views") + 1
            queryset2.save()
            # bundan dolayı okuma hemen 1 artmış olmaz
        # açılan makale bittikten sonra okunulan liste altındaki diğer paylaşımları anasayfadaki gibi listeler
    content_id = queryset.id
    nav_category = ctof(user = content_user,content_list = utopic)
    nav_list = []
    for nav in nav_category: # şuan okuduğu yazının öncesi
        if nav.id < content_id:
            if len(nav_list) < 6:
                nav_list.append(nav)
    nav_list.append(queryset) # şuan okuduğu yazı
    for nav in nav_category: # sonrası
        if nav.id > content_id:
            if len(nav_list) < 3:
                nav_list.append(nav)
    nav_category = nav_list
    info_of_cards = content_cards(request,nav_category,5)
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
        content = Content.objects.filter(url = content_path)[0]
        Comment(user=user,comment=comment,content = content).save()
        query = Content.objects.filter(url = content_path)[0]
        query.hmanycomment = F("hmanycomment")+1
        query.save()
        if str(content.user) != str(user.username):
            Notification(user=content.user,even = 1,content=comment,address = content_path).save()
        return HttpResponse(
            json.dumps({
                "comment": comment,
                "username":request.user.username,
                "date":1,
                "img":get_head_img_pp(request.user)[0]
            })
        )
