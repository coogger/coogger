#django
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages
from django.db.models import F
from django.db.models import Q
from django.contrib import messages as ms

#models
from cooggerapp.models import Content,OtherInformationOfUsers,Notification,SearchedWords,Following

#views
from cooggerapp.views.tools import paginator,hmanynotifications,content_cards

def home(request):
    info_of_cards = content_cards(request,hmany=10)
    context = dict(
    content = info_of_cards[0],
    paginator = info_of_cards[1],
    hmanynotifications = hmanynotifications(request),
    )
    template = "card/blogs.html"
    return render(request,template,context)

def following_content(request):
    oof = []
    for i in Following.objects.filter(user = request.user):
        i_wuser = i.which_user
        oof.append(i.which_user)
    query = []
    for q in Content.objects.all():
        if q.user in oof:
            query.append(q)
    info_of_cards = content_cards(request,query,hmany=10)
    context = dict(
    content = info_of_cards[0],
    paginator = info_of_cards[1],
    hmanynotifications = hmanynotifications(request),
    )
    template = "card/blogs.html"
    return render(request,template,context)

def search(request):
    query = request.GET["query"].lower()
    q = Q(title__contains = query) | Q(content_list__contains = query) | Q(tag__contains = query)
    queryset = Content.objects.filter(q).order_by("-views")
    info_of_cards = content_cards(request,queryset,hmany=20)
    data_search = SearchedWords.objects.filter(word = query)
    if data_search.exists():
        data_search = data_search[0]
        data_search.hmany = F("hmany")+1
        data_search.save()
    else:
        SearchedWords(word = query).save()
    context = dict(
        content = info_of_cards[0],
        paginator = info_of_cards[1],
    )
    template = "card/blogs.html"
    return render(request,template,context)

def notification(request):
    try:
        queryset = Notification.objects.filter(user = request.user).order_by("-time")
        hmanynotifications = queryset.filter(show=False).count()
        queryset.update(show = True)
    except:
        ms.error(request,"Bildirimleri görmeniz için giriş yapın hesabınız yoksa üye olun")
        return HttpResponseRedirect("/")
    pagi = paginator(request,queryset,10)
    context = dict(
        notifications = pagi,
        paginator = pagi,
        hmanynotifications = hmanynotifications,
        )
    template = "home/notifications.html"
    return render(request,template,context)
