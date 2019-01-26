# django
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

# models
from core.cooggerapp.models import OtherAddressesOfUsers
from core.steemconnect_auth.models import Dapp

def content_by_filter(items, queryset):
    filter = ""
    for attr, value in items:
        filter += f"&{attr}={value}"
        if attr == "username":
            value = get_user(username=value)
            attr = "user"
        elif attr == "dapp":
            value = Dapp.objects.filter(name=value)[0]
        if attr == "tags":
            try:
                self.queryset = self.queryset.filter(tags__contains = value)
            except FieldError:
                pass
        else:
            queryset = queryset.filter(**{attr: value})
    return dict(filter=filter, queryset=queryset)

def get_user(username):
    return User.objects.filter(username=username)[0]

def user_topics(queryset):
    topics = []
    for query in queryset:
        topic = query.topic
        if topic not in topics:
            topics.append(topic)
    return topics


def make_choices_slug(choice):
    "choice bir liste olacak gelen listeyi choices'e uygun hale getirir"
    slugs = []
    for cho in choice:
        cho = cho.lower()
        cho = slugify(cho)
        slugs.append((cho, cho))
    return slugs


def paginator(request, queryset, hmany=settings.PAGE_SIZE):
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
        user_follow = OtherAddressesOfUsers.objects.filter(user=user)
    except:
        user_follow = []
    return user_follow


def get_facebook(user):
    facebook = None
    try:
        for f in users_web(user):
            if f.choices == "facebook":
                facebook = f.adress
    except:
        pass
    return facebook
