# django
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.exceptions import FieldError
from django.contrib.auth import authenticate

# models
from core.cooggerapp.models import Topic


def content_by_filter(items, queryset):
    filter = ""
    for attr, value in items:
        filter += f"&{attr}={value}"
        if attr == "username":
            value = authenticate(username=value)
            attr = "user"
        elif attr == "tags":
            queryset = queryset.filter(tags__contains = value)
        else:
            try:
                queryset = queryset.filter(**{attr: value})
            except FieldError:
                pass
    return dict(filter=filter, queryset=queryset)

def user_topics(queryset):
    topics = []
    for query in queryset:
        topic_obj = Topic.objects.filter(name=query.topic)[0]
        if topic_obj not in topics:
            topics.append(topic_obj)
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
