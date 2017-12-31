from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from cooggerapp.models import OtherInformationOfUsers,Notification,Content,UserFollow
from cooggerapp.choices import *
from bs4 import BeautifulSoup



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

def get_head_img_pp(user):
    pp = OtherInformationOfUsers.objects.filter(user = user)[0].pp
    if pp:
        img = "/media/users/pp/pp-"+user.username+".jpg"
    else:
        img = "/static/media/profil.png"
    return [img,pp]

def get_pp_from_contents(queryset):
    "dekoratör"
    for p in queryset:
        user = User.objects.filter(username = p.user)[0]
        is_pp = OtherInformationOfUsers.objects.filter(user = user)[0].pp
        yield is_pp

def get_ip(request):
    try:
        ip = request.META["HTTP_X_FORWARDED_FOR"].split(',')[-1].strip()
    except:
        return None
    return ip

def hmanynotifications(request):
    try:
        queryset = Notification.objects.filter(user = request.user)
    except:
        return False
      # görmediği kaç bildirim olduğu sayısı
    return queryset.filter(show = False).count()

def content_cards(request,queryset = Content.objects.all(),hmany = 10):
    "içerik kartlarının gösterilmesi için gerekli olan bütün bilgilerin üretildiği yer"
    paginator_of_cards = paginator(request,queryset,hmany)
    pp_in_cc = [pp for pp in get_pp_from_contents(paginator_of_cards)]
    cards = zip(paginator_of_cards,pp_in_cc)
    return cards,paginator_of_cards # cardlar için gereken bütün bilgiler burda

def users_web(user):
    try:
        user_follow = UserFollow.objects.filter(user = user)
    except:
        user_follow = []
    return user_follow

def get_facebook(user):
    facebook = None
    try:
        for f in users_web(user):
            if f.choices  == "facebook":
                facebook = f.adress
    except:
        pass
    return facebook

def html_head(queryset):
    head = dict(
    title = queryset.title + " | coogger",
    keywords = queryset.tag,
    description = queryset.show,
    author = get_facebook(queryset.user),
    )
    return head
