from cooggerapp.choices import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from cooggerapp import models
from django.utils.text import slugify

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
        user = User.objects.filter(username = p.username)[0]
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

def take_subcategory(request,value,permission=False):
    "value ile gelen fields kodunu alıp ilgili bir alt dalı seçip gönderiyorum"
    if not request.is_ajax() and not permission:
        return None
    values = []
    for i in dir(Subcategory): # burada gelen value bilgisini kontrol ediyoruz ki istenmeyen bir value gelmesin
        if not i.startswith("__"):
            values.append(i)
    value = value.replace("-","_")
    if value not in values:
        subcategory = None
    else:
        subcategory = make_choices(eval("Subcategory."+value+"()"))
    return subcategory

def take__category2(request,value,permission=False):
    if not request.is_ajax():
        return None
    values = []
    for i in dir(Category2): # burada gelen value bilgisini kontrol ediyoruz ki istenmeyen bir value gelmesin
        if not i.startswith("__"):
            values.append(i)
    value = value.replace("-","_")
    if value not in values:
        category2 = None
    category2 = make_choices(eval("Category2."+value+"()"))
    return category2

def hmanynotifications(request):
    try:
        queryset = models.Notification.objects.filter(user = request.user)
    except:
        return False
      # görmediği kaç bildirim olduğu sayısı
    return queryset.filter(show = False).count()
