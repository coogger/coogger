#django
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#models
from apps.cooggerapp.models import UserFollow

#choices seçimler
from apps.cooggerapp.choices import *

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
    description = queryset.definition,
    author = get_facebook(queryset.user),
    )
    return head
