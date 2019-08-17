from django.conf import settings
from django.core.exceptions import FieldError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def paginator(request, queryset, how_many=settings.PAGE_SIZE):
    paginator = Paginator(queryset, how_many)
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
    _filter = ""
    first = True
    for attr, value in items:
        if attr == "page":
            continue
        if first:
            first = False
            _filter += f"?{attr}={value}"
        else:
            _filter += f"&{attr}={value}"
        if attr == "username":
            queryset = queryset.filter(user__username=value)
        elif attr == "tags":
            queryset = queryset.filter(tags__contains=value)
        elif attr == "category":
            queryset = queryset.filter(category__name=value)
        elif attr == "topic":
            queryset = queryset.filter(utopic__permlink=value)
        else:
            try:
                queryset = queryset.filter(**{attr: value})
            except FieldError:
                pass
    return dict(filter=_filter, queryset=queryset)
