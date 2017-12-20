from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages
from django.db.models import F
from cooggerapp.models import Content
from cooggerapp.views.tools import paginator,hmanynotifications
from cooggerapp.views.home import content_cards
from django.db.models import Q

def hashtag(request,hashtag):
    queryset = Content.objects.filter(tag__contains = hashtag)
    info_of_cards = content_cards(request,queryset)
    elastic_search = dict(
     title ="#"+hashtag+" | coogger",
     keywords = hashtag,
     description = hashtag +" konu etiketi altında ki bütün coogger bilgilerini gör",
    )
    output = dict(
        blog = info_of_cards[0],
        general = True,
        nameofhashtag = hashtag,
        ogurl = request.META["PATH_INFO"],
        paginator = info_of_cards[1],
        elastic_search = elastic_search,
        hmanynotifications = hmanynotifications(request),
    )
    return render(request,"blog/blogs.html",output)

def list(request,list_):
    queryset = Content.objects.filter(content_list = list_)
    info_of_cards = content_cards(request,queryset)
    elastic_search = dict(
     title = list_,
     keywords = list_,
     description = list_ +" liste etiketi altında ki bütün coogger bilgilerini gör",
    )
    output = dict(
        blog = info_of_cards[0],
        general = True,
        ogurl = request.META["PATH_INFO"],
        nameoflist_ex = list_,
        paginator = info_of_cards[1],
        hmanynotifications = hmanynotifications(request),
        elastic_search = elastic_search,
    )
    return render(request,"blog/blogs.html",output)
