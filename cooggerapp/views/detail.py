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
from cooggerapp.models import Content,Contentviews,UserFollow,Voters,Comment,Notification
from cooggerapp.views.tools import (get_ip,html_head,get_head_img_pp,content_cards,hmanynotifications,users_web)


def main_detail(request,blog_path,utopic,path):
    "blogların detay kısmı "
    ip = get_ip(request)
    ctof = Content.objects.filter
    queryset = ctof(url = blog_path)[0]
    content_user = queryset.user
    if not Contentviews.objects.filter(content = queryset,ip = ip).exists():
        Contentviews(content = queryset,ip = ip).save()
        queryset2 = queryset # değişeceği için kopyalıyorum
        queryset.views = F("views") + 1
        queryset.save()
        queryset = queryset2 # değiştikten sonra yine eski değerine atıyorum
        # bundan dolayı okuma hemen 1 artmış olmaz
        del queryset2 # silelim
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
    stars = stars(queryset),
    content = info_of_cards[0],
    detail = queryset,
    global_hashtag = [i for i in queryset.tag.split(",") if i != ""],
    comment_form = Comment.objects.filter(content=queryset),
    hmanynotifications = hmanynotifications(request),
    user_follow = users_web(content_user),
    )
    template = "detail/main_detail.html"
    return render(request,template,context)

def stars(queryset):
    try:
        stars_ = str(int(queryset.stars/queryset.hmstars))
    except ZeroDivisionError:
        stars_ = ""
    return stars_

def give_stars(request,post_id,stars_id):
    if not request.is_ajax():
        return None
    if not request.user.is_authenticated:
        return HttpResponse("Oy vermek için giriş yapmalı veya üye olmalısınız")
    user = request.user
    request_username = user.username
    ctof = Content.objects.filter
    blog = ctof(id = post_id)[0]
    blog2 = blog
    try:
        vot = Voters.objects.filter(user = user,content = blog) # daha önceden verdiği oy varsa alıyoruz
        old = vot[0].star
        vot.update(star = stars_id)
        blog.stars = F("stars")-old+stars_id
        blog.save()
    except IndexError: # ilk kez oylama yapıyor
        Voters(user = user,content = blog,star = stars_id).save()
        blog.hmstars = F("hmstars")+1
        blog.stars = F("stars")+stars_id
        blog.save()
    if str(blog.user) != str(user.username):
        Notification(user=blog.user,even = 2,content=str(int(stars_id)+1),address = blog.url).save()
    first_li = """<li class="d-starts-li" data-starts-id="{{i}}" data-post-id="""+ post_id+ """><img class="d-starts-a" src="/static/media/icons/star.svg"></li>"""
    second_li="""<li class="d-starts-li" data-starts-id="{{i}}" data-post-id="""+ post_id+ """><img class="d-starts-a" src="/static/media/icons/star(0).svg"></li>"""
    output = ""
    blog = ctof(id = post_id)[0]
    stars = blog.stars
    hmstars = blog.hmstars
    rate = stars/hmstars
    for i in range(1,6,1):
        if i <= int(rate):
            output += first_li.replace("{{i}}",str(i))
        if i > int(rate):
            output += second_li.replace("{{i}}",str(i))
        if i == 5:
            output = "<ul class='d-starts-ul' data-gnl='1 1p ortada'>"+output+"</ul>"
            output +="<div style='text-align: -webkit-left;width: 160px;margin: auto;margin-top: 9px;float: left;cursor: pointer;'>Verilen oy sayısı : "+str(hmstars)+"</div>"
            output +="<div  class='gstars' style='text-align: -webkit-left;width: 160px;margin: auto;margin-top: 9px;float: left;cursor: pointer;'>Oy ortalaması : "+str(int(rate))+"</div>"
    return HttpResponse(output)

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
