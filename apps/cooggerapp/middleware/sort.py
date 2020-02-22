from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin
from django.utils.text import slugify

from ..choices import LANGUAGES
from ..models import Content
from ..views.utils import model_filter


class SortMiddleware(MiddlewareMixin):
    valid_urls = [
        "index",
        "filter",
        "language",
        "topic",
        "search",
        "explorer_posts",
        "feed",
    ]

    def process_request(self, request):
        request.sort_languages = self.sort_languages(request)
        request.languages = self.languages(request)

    @staticmethod
    def get_url_name(request):
        return resolve(request.path_info).url_name

    def get_queryset(self, request):
        try:
            name = request.path_info.split("/")[2]
        except IndexError:
            return None
        queryset = Content.objects.filter(status="ready")
        url_name = self.get_url_name(request)
        if url_name == "topic":
            queryset = queryset.filter(utopic__permlink=name)
        elif url_name == "language":
            queryset = queryset.filter(language=name)
        elif url_name == "hashtag":
            queryset = queryset.filter(tags__contains=name)
        elif url_name == "filter":
            queryset = model_filter(request.GET.items(), queryset).get("queryset")
        else:
            return None
        return queryset

    @staticmethod
    def sort_list(queryset):
        context = []
        for query in sorted(queryset, key=len, reverse=True):
            name = str(query[0].language).lower()
            try:
                context.append((name, len(query)))
            except IndexError:
                pass
        return context

    def sort_languages(self, request):
        queryset = self.get_queryset(request)
        if queryset is None:
            return None
        queryset_list = []
        for language in LANGUAGES:
            querysets = queryset.filter(language=language)
            if querysets.exists():
                queryset_list.append(querysets)
        return self.sort_list(queryset_list)

    def languages(self, request):
        url_name = self.get_url_name(request)
        if url_name not in self.valid_urls:
            return None
        querysets_list = []
        content_queryset = Content.objects.filter(status="ready")
        for language in LANGUAGES:
            querysets = content_queryset.filter(language=language)
            if querysets.exists():
                querysets_list.append(querysets)
        context = []
        for contents in sorted(querysets_list, key=len, reverse=True):
            try:
                context.append(
                    (slugify(contents[0].language), str(contents[0].language).lower())
                )
            except IndexError:
                pass
        return context
