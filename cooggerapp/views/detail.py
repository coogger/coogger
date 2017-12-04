from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages
from django.contrib.auth.models import User
from cooggerapp.models import Blog,Blogviews,OtherInformationOfUsers,UserFollow,Voters,Comment,Notification
from cooggerapp.views.tools import Topics,get_ip,paginator,get_pp_from_contents,get_stars_from_contents
from django.db.models import F
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
from django.utils.text import slugify
import json
import os
from django.utils import timezone


def main_detail(request,blog_path,utopic,path):
    "blogların detay kısmı "
    queryset = Blog.objects.filter(url = blog_path)[0]
    username_id = queryset.username_id
    user = User.objects.filter(id = username_id)[0]
    ip = get_ip(request)
    nav_category = [nav for nav in nav_category_for_detail(username_id,utopic)]
    if not Blogviews.objects.filter(content = queryset,ip = ip).exists():
        Blogviews(content = queryset,ip = ip).save()
        queryset.views = F("views") + 1
        queryset.save()
        queryset = Blog.objects.filter(url = blog_path)[0]
    try:
        stars = str(int(queryset.stars/queryset.hmstars))
    except ZeroDivisionError:
        stars = ""
    facebook = get_facebook(user)
    elastic_search = dict(
        title = queryset.title+" | coogger",
        keywords = queryset.tag +","+user.username+" "+utopic+", "+utopic+",coogger "+queryset.category+", "+queryset.title,
        description = queryset.show,
        author = facebook,
    )
    output = dict(
        detail = queryset,
        elastic_search = elastic_search,
        general = True,
        username  = user,
        stars = stars,
        nameoftopic = queryset.title,
        nav_category = nav_category,
        nameoflist = utopic,
        ogurl = request.META["PATH_INFO"],
        global_hashtag = [i for i in queryset.tag.split(",") if i != ""],
        comment_form = Comment.objects.filter(content=queryset),
    )
    # açılan makale bittikten sonra okunulan liste altındaki diğer paylaşımları anasayfadaki gibi listeler
    query = Blog.objects.filter(username = username_id,content_list = utopic)
    info_of_cards = content_cards(request,query,6)
    output["blog"] = info_of_cards[0]
    output["paginator"] = info_of_cards[1]
    return render(request,"detail/main_detail.html",output)

def stars(request,post_id,stars_id):
    if not request.is_ajax():
        return None
    if not request.user.is_authenticated:
        return HttpResponse("Oy vermek için giriş yapmalı veya üye olmalısınız")
    user = request.user
    request_username = user.username
    blog = Blog.objects.filter(id = post_id)[0]
    try:
        vot = Voters.objects.filter(user = user,blog = blog) # daha önceden verdiği oy varsa alıyoruz
        old = vot[0].star
        vot.update(star = stars_id)
        blog.stars = F("stars")-old+stars_id
        blog.save()
    except IndexError: # ilk kez oylama yapıyor
        Voters(user = user,blog = blog,star = stars_id).save()
        blog.hmstars = F("hmstars")+1
        blog.stars = F("stars")+stars_id
        blog.save()
    if str(blog.username) != str(user.username):
        Notification(user=blog.username,even = 2,content=str(int(stars_id)+1),address = blog.url).save()
    first_li = """<li class="d-starts-li" data-starts-id="{{i}}" data-post-id="""+ post_id+ """><img class="d-starts-a" src="/static/media/icons/star.svg"></li>"""
    second_li="""<li class="d-starts-li" data-starts-id="{{i}}" data-post-id="""+ post_id+ """><img class="d-starts-a" src="/static/media/icons/star(0).svg"></li>"""
    output = ""
    blog = Blog.objects.filter(id = post_id)[0]
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
            output +="<div  data-gnl='1 1p ortada'>Verilen oy sayısı : "+str(hmstars)+"</div>"
            output +="<div  class='gstars' data-gnl='1 1p ortada'>Oy ortalaması : "+str(int(rate))+"</div>"
    return HttpResponse(output)

def comment(request,content_path):
    if request.method=="POST" and request.is_ajax() and request.user.is_authenticated:
        user = request.user
        comment = request.POST["comment"]
        content = Blog.objects.filter(url = content_path)[0]
        Comment(user=user,comment=comment,content = content).save()
        query = Blog.objects.filter(url = content_path)[0]
        query.hmanycomment = F("hmanycomment")+1
        query.save()
        if str(content.username) != str(user.username):
            Notification(user=content.username,even = 1,content=comment,address = content_path).save()
        return HttpResponse(
            json.dumps({
                "comment": comment,
                "username":request.user.username,
                "date":1,
                "img":get_head_img_pp(request.user)[0]
            })
        )

def get_head_img_pp(user):
    pp = OtherInformationOfUsers.objects.filter(user = user)[0].pp
    if pp:
        img = "/media/users/pp/pp-"+user.username+".jpg"
    else:
        img = "/static/media/profil.png"
    return [img,pp]

def get_facebook(user):
    facebook = None
    try:
        for f in UserFollow.objects.filter(user = user):
            if f.choices  == "facebook":
                facebook = f.adress
    except:
        pass
    return facebook

def nav_category_for_detail(username_id,utopic):
    nav_category = Blog.objects.filter(username = username_id,content_list = utopic)
    for category in nav_category:
       yield category.url,category.title

def content_cards(request,queryset,hmany):
    "içerik kartlarının gösterilmesi için gerekli olan bütün bilgilerin üretildiği yer"
    paginator_of_cards = paginator(request,queryset,hmany)
    pp_in_cc = [pp for pp in get_pp_from_contents(paginator_of_cards)]
    stars = [s for s in get_stars_from_contents(paginator_of_cards)]
    cars = zip(paginator_of_cards,pp_in_cc,stars)
    return cars,paginator_of_cards # cardlar için gereken bütün bilgiler burda
