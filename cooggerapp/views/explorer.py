#django
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages as ms

#models
from cooggerapp.models import Content

#views
from cooggerapp.views.tools import paginator,hmanynotifications

def hashtag(request,hashtag):
    if hashtag == "":
        ms.error(request,"Boş etiket girdiniz !")
        return HttpResponseRedirect("/")
    queryset = Content.objects.filter(tag__contains = hashtag, confirmation = True)
    if not queryset:
        ms.error(request,"{} etiketi henüz coogger'da bulunmuyor!".format(hashtag))
        return HttpResponseRedirect("/")
    info_of_cards = paginator(request,queryset,10)
    html_head = dict(
     title = hashtag+" | coogger",
     keywords = hashtag,
     description = hashtag +" konu etiketi altında ki bütün coogger bilgilerini gör",
    )
    context = dict(
        content = info_of_cards,
        nameofhashtag = hashtag,
        head = html_head,
        hmanynotifications = hmanynotifications(request),
    )
    template = "card/blogs.html"
    return render(request,template,context)

def users_list(request,list_):
    if list_ == "":
        ms.error(request,"Boş liste girdiniz !")
        return HttpResponseRedirect("/")
    queryset = Content.objects.filter(content_list = list_, confirmation = True)
    if not queryset:
        ms.error(request,"{} listesi henüz coogger'da bulunmuyor!".format(list_))
        return HttpResponseRedirect("/")
    info_of_cards = paginator(request,queryset,10)
    html_head = dict(
     title = list_ +" | coogger",
     keywords = list_,
     description = list_ +" liste etiketi altında ki bütün coogger bilgilerini gör",
    )
    context = dict(
        content = info_of_cards,
        nameoflist_ex = list_,
        hmanynotifications = hmanynotifications(request),
        head = html_head,
    )
    template = "card/blogs.html"
    return render(request,template,context)
