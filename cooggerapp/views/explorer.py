from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from cooggerapp.models import Content
from cooggerapp.views.tools import paginator,hmanynotifications,content_cards

def hashtag(request,hashtag):
    queryset = Content.objects.filter(tag__contains = hashtag)
    info_of_cards = content_cards(request,queryset)
    html_head = dict(
     title ="#"+hashtag+" | coogger",
     keywords = hashtag,
     description = hashtag +" konu etiketi altında ki bütün coogger bilgilerini gör",
    )
    context = dict(
        content = info_of_cards[0],
        nameofhashtag = hashtag,
        paginator = info_of_cards[1],
        head = html_head,
        hmanynotifications = hmanynotifications(request),
    )
    template = "card/blogs.html"
    return render(request,template,context)

def users_list(request,list_):
    queryset = Content.objects.filter(content_list = list_)
    info_of_cards = content_cards(request,queryset)
    html_head = dict(
     title = list_,
     keywords = list_,
     description = list_ +" liste etiketi altında ki bütün coogger bilgilerini gör",
    )
    context = dict(
        content = info_of_cards[0],
        nameoflist_ex = list_,
        paginator = info_of_cards[1],
        hmanynotifications = hmanynotifications(request),
        head = html_head,
    )
    template = "card/blogs.html"
    return render(request,template,context)
