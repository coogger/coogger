# django
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import FieldError

# models
from ..models import Category, Topic


def paginator(request, queryset):
    paginator = Paginator(queryset, settings.PAGE_SIZE)
    page = request.GET.get("page")
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return contacts


def model_filter(items, queryset):
    # TODO improved this function
    filter = ""
    first = True
    for attr, value in items:
        if attr == "page":
            continue
        if first:
            first = False
            filter += f"?{attr}={value}"
        else:
            filter += f"&{attr}={value}"
        if attr == "username":
            queryset = queryset.filter(user__username=value)
        elif attr == "tags":
            queryset = queryset.filter(tags__contains=value)
        elif attr == "category":
            queryset = queryset.filter(category__name=value)
        elif attr == "topic":
            queryset = queryset.filter(utopic__permlink=value)
        elif attr == "reply" and value == "None":
            queryset = queryset.filter(reply=None)
        else:
            try:
                queryset = queryset.filter(**{attr: value})
            except FieldError:
                pass
    return dict(filter=filter, queryset=queryset)
