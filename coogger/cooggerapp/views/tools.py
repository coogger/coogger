# django
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# models
from cooggerapp.models import OtherAddressesOfUsers, Content

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


def paginator(request, queryset, hmany=6):
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
