from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages
from django.db.models import F
from cooggerapp.models import Blog,OtherInformationOfUsers,Notification,SearchedWords
from cooggerapp.views.tools import get_pp_from_contents,get_stars_from_contents,paginator,hmanynotifications
from django.db.models import Q
from django.contrib import messages as ms

def home(request):
    info_of_cards = content_cards(request,hmany=10)
    output = dict(
        blog = info_of_cards[0],
        #nav_category = category, bu isim ile veriliyor unutma
        general = True,
        ogurl = request.META["PATH_INFO"],
        paginator = info_of_cards[1],
        hmanynotifications = hmanynotifications(request),
        )
    return render(request,"blog/blogs.html",output)


def search(request):
    query = request.GET["query"].lower()
    q = Q(title__contains = query) | Q(content_list__contains = query) | Q(tag__contains = query)
    queryset = Blog.objects.filter(q).order_by("-views")
    info_of_cards = content_cards(request,queryset,hmany=20)
    data_search = SearchedWords.objects.filter(word = query)
    if data_search.exists():
        data_search = data_search[0]
        data_search.hmany = F("hmany")+1
        data_search.save()
    else:
        SearchedWords(word = query).save()
    output = dict(
        blog = info_of_cards[0],
        general = True,
        ogurl = request.META["PATH_INFO"],
        paginator = info_of_cards[1],
    )
    return render(request,"blog/blogs.html",output)

def notification(request):
    try:
        queryset = Notification.objects.filter(user = request.user).order_by("-time")
        hmanynotifications = queryset.filter(show=False).count()
        queryset.update(show = True)
    except:
        ms.error(request,"Bildirimleri görmeniz için giriş yapın hesabınız yoksa üye olun")
        return HttpResponseRedirect("/")
    pagi = paginator(request,queryset,10)
    output = dict(
        notifications = pagi,
        general = True,
        paginator = pagi,
        hmanynotifications = hmanynotifications,
        )
    return render(request,"home/notifications.html",output)

def content_cards(request,queryset = Blog.objects.all(),hmany = 10):
    "içerik kartlarının gösterilmesi için gerekli olan bütün bilgilerin üretildiği yer"
    paginator_of_cards = paginator(request,queryset,hmany)
    pp_in_cc = [pp for pp in get_pp_from_contents(paginator_of_cards)]
    stars = [s for s in get_stars_from_contents(paginator_of_cards)]
    cards = zip(paginator_of_cards,pp_in_cc,stars)
    return cards,paginator_of_cards # cardlar için gereken bütün bilgiler burda
