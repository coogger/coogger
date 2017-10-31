from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages
from django.db.models import F
from cooggerapp.models import Blog
from cooggerapp.views.tools import paginator,Topics,get_head_img_pp
from cooggerapp.views.home import content_cards
from django.db.models import Q

def hashtag(request,hashtag):
    queryset = Blog.objects.filter(tag__regex = hashtag)
    username = request.user.username
    info_of_cards = content_cards(request,queryset)
    category = Topics().category   
    try:
        img_pp = get_head_img_pp(request.user)
    except:
        img_pp = ["/static/media/profil.png",None]
    elastic_search = dict(
     title ="#"+hashtag+" | coogger",
     keywords = hashtag,
     description = hashtag +" konu etiketi altında ki bütün coogger bilgilerini gör",
     img="/static/media/icons/hashtag.svg",
    )
    output = dict(
        blog = info_of_cards[0],
        nav_category = category,
        general = True,
        img = img_pp[0],
        username = username,
        nameofhashtag = hashtag,
        ogurl = request.META["PATH_INFO"],
        paginator = info_of_cards[1],
        elastic_search = elastic_search,
    )
    return render(request,"blog/blogs.html",output)

def list(request,list):
    queryset = Blog.objects.filter(content_list = list)
    username = request.user.username
    info_of_cards = content_cards(request,queryset)
    category = Topics().category
    try:
        img_pp = get_head_img_pp(request.user)
    except:
        img_pp = ["/static/media/profil.png",None]
    elastic_search = dict(
     title = list +" | coogger",
     keywords = list,
     description = list +" liste etiketi altında ki bütün coogger bilgilerini gör",
     img="/static/media/icons/list.svg",
    )
    output = dict(
        blog = info_of_cards[0],
        nav_category = category,
        general = True,
        img = img_pp[0],
        username = username,
        ogurl = request.META["PATH_INFO"],
        nameoflist_ex = list,
        paginator = info_of_cards[1],
        elastic_search = elastic_search,
    )
    return render(request,"blog/blogs.html",output)
