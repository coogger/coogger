# django
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.conf import settings
from django.core.exceptions import FieldError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# models
from core.cooggerapp.models import Category, Topic


def paginator(request, queryset):
    paginator = Paginator(queryset, settings.PAGE_SIZE)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return contacts

def model_filter(items, queryset):
    filter = ""
    for attr, value in items:
        filter += f"&{attr}={value}"
        if attr == "username":
            queryset = queryset.filter(user = User.objects.get(username=username))
        elif attr == "tags":
            queryset = queryset.filter(tags__contains = value)
        elif attr == "category":
            category = Category.objects.filter(name=value)[0]
            queryset = queryset.filter(category = category)
        elif attr == "topic":
            topic = Topic.objects.filter(name=value)[0]
            queryset = queryset.filter(topic = topic)
        else:
            try:
                queryset = queryset.filter(**{attr: value})
            except FieldError:
                pass
    return dict(filter=filter, queryset=queryset)

def make_choices_slug(choice):
    "choice bir liste olacak gelen listeyi choices'e uygun hale getirir"
    slugs = []
    for cho in choice:
        cho = cho.lower()
        cho = slugify(cho)
        slugs.append((cho, cho))
    return slugs
