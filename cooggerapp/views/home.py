#django
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages
from django.db.models import F
from django.db.models import Q
from django.contrib import messages as ms

#form
from cooggerapp.forms import ReportsForm

#models
from cooggerapp.models import Content,OtherInformationOfUsers,Notification,SearchedWords,Following

#views
from cooggerapp.views.tools import paginator,hmanynotifications

def home(request):
    queryset = Content.objects.filter(confirmation = True)
    info_of_cards = paginator(request,queryset,20)
    context = dict(
    content = info_of_cards,
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
    for q in Content.objects.filter(confirmation = True):
        if q.user in oof:
            query.append(q)
    info_of_cards = paginator(request,query,10)
    context = dict(
    content = info_of_cards,
    hmanynotifications = hmanynotifications(request),
    )
    template = "card/blogs.html"
    return render(request,template,context)

def search(request):
    query = request.GET["query"].lower()
    q = Q(title__contains = query) | Q(content_list__contains = query) | Q(tag__contains = query)
    queryset = Content.objects.filter(q,confirmation = True).order_by("-views")
    info_of_cards = paginator(request,queryset,20)
    data_search = SearchedWords.objects.filter(word = query)
    if data_search.exists():
        data_search = data_search[0]
        data_search.hmany = F("hmany") + 1
        data_search.save()
    else:
        SearchedWords(word = query).save()
    context = dict(
        content = info_of_cards,
    )
    template = "card/blogs.html"
    return render(request,template,context)

def notification(request):
    try:
        queryset = Notification.objects.filter(user = request.user).order_by("-time")
        queryset.update(show = True)
    except:
        return HttpResponseRedirect("/")
    pagi = paginator(request,queryset,10)
    context = dict(
        notifications = pagi,
        hmanynotifications = queryset.filter(show=False).count(),
        )
    template = "home/notifications.html"
    return render(request,template,context)

def report(request):
    request_user = request.user
    if not request_user.is_authenticated:
        return HttpResponseRedirect("/")
    form = ReportsForm(request.POST)
    if form.is_valid():
        form  = form.save(commit=False)
        form.user = request.user
        form.content = Content.objects.filter(id = request.POST["content_id"])[0]
        form.save()
        ms.error(request,"Şikayetiniz alınmıştır.")
        return HttpResponseRedirect("/")
    context = dict(
    report_form = form,
    content_id = request.GET["content_id"],
    )
    template = "home/report.html"
    return render(request,template,context)
