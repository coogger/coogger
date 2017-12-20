from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from cooggerapp import models
from cooggerapp.choices import *

from bs4 import BeautifulSoup

def make_choices(choice):
    "choice bir liste olacak gelen listeyi choices'e uygun hale getirir"
    slugs = []
    for cho in choice:
        cho = str(cho).lower()
        slugs.append((slugify(cho),cho))
    return slugs

def make_choices_slug(choice):
    "choice bir liste olacak gelen listeyi choices'e uygun hale getirir"
    slugs = []
    for cho in choice:
        cho = cho.lower()
        cho = slugify(cho)
        slugs.append((cho,cho))
    return slugs

def paginator(request,queryset,hmany=20):
    paginator = Paginator(queryset, hmany)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return contacts

def seo(request):
    "arama motoru optimizasyonu için robot.txt ve site haritası"
    file = request.get_full_path()
    return render(request,"seo/"+file,{})

def durationofread(text):
    reading_speed = 20 # 1 saniyede 20 harf okunursa
    read_content = BeautifulSoup(text, 'html.parser').get_text().replace(" ","")
    how_much_words = len(read_content)
    words_time = float((how_much_words/reading_speed)/60)
    return str(words_time)[:3]

def get_pp_from_contents(queryset):
    "dekoratör"
    for p in queryset:
        user = User.objects.filter(username = p.user)[0]
        is_pp = models.OtherInformationOfUsers.objects.filter(user = user)[0].pp
        yield is_pp

def get_stars_from_contents(queryset):
    "dekoratör"
    for i in queryset:
        try:
            yield str(int(i.stars/i.hmstars))
        except ZeroDivisionError:
            yield "0"

def get_ip(request):
    try:
        ip = request.META["HTTP_X_FORWARDED_FOR"].split(',')[-1].strip()
    except:
        ip = request.META['REMOTE_ADDR']
    return ip

def hmanynotifications(request):
    try:
        queryset = models.Notification.objects.filter(user = request.user)
    except:
        return False
      # görmediği kaç bildirim olduğu sayısı
    return queryset.filter(show = False).count()
