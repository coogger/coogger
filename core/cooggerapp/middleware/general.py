from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.urls import resolve
from django.utils.text import slugify

# models.
from core.cooggerapp.models import Category, Content, Topic

# coices
from core.cooggerapp.choices import *

from core.cooggerapp.utils import model_filter

class GeneralMiddleware(MiddlewareMixin):

    def process_request(self, request):
        self.path_info = request.path_info
        invalid = ["sitemap", "api", "robots.txt"]
        if self.path_info.split("/")[1] in invalid:
            return None
        url_name = resolve(self.path_info).url_name
        request.sort_categories = self.sort_categories(request, url_name)
        request.sort_languages = self.sort_languages(request, url_name)
        request.categories = self.categories(request)
        request.languages = self.languages(request)
        if url_name in ["home", "search", "explorer_posts"]:
            request.sort_topics = self.sort_topics(request)
        request.settings = settings

    def sort_categories(self, request, url_name):
        category_queryset = Category.objects.all()
        querysets_list = []
        content_queryset = Content.objects.filter(status="approved")
        try:
            name = self.path_info.split("/")[2]
        except IndexError:
            return None
        if url_name == "category":
            category = Category.objects.filter(name=name)[0]
            content_queryset = content_queryset.filter(category=category)
        elif url_name == "topic":
            topic = Topic.objects.filter(name=name)[0]
            content_queryset = content_queryset.filter(topic=topic)
        elif url_name == "language":
            content_queryset = content_queryset.filter(language=name)
        elif url_name == "filter":
            content_queryset = model_filter(request.GET.items(), content_queryset).get("queryset")
        for category in category_queryset:
            querysets = content_queryset.filter(category=category)
            try:
                querysets[0]
            except:
                pass
            else:
                querysets_list.append(querysets)
        context = []
        for contents in sorted(querysets_list, key=len, reverse=True):
            try:
                context.append(
                    (
                        slugify(contents[0].category),
                        str(contents[0].category).lower(),
                        len(contents)
                        )
                    )
            except IndexError:
                pass
        return context

    def languages(self, request):
        querysets_list = []
        content_queryset = Content.objects.filter(status="approved")
        for language in languages:
            querysets = content_queryset.filter(language = language)
            try:
                querysets[0]
            except:
                pass
            else:
                querysets_list.append(querysets)
        context = []
        for contents in sorted(querysets_list, key=len, reverse=True):
            try:
                context.append((slugify(contents[0].language), str(contents[0].language).lower()))
            except IndexError:
                pass
        return context

    def categories(self, request):
        category_queryset = Category.objects.all()
        querysets_list = []
        content_queryset = Content.objects.filter(status="approved")
        for category in category_queryset:
            querysets = content_queryset.filter(category=category)
            try:
                querysets[0]
            except:
                pass
            else:
                querysets_list.append(querysets)
        context = []
        for contents in sorted(querysets_list, key=len, reverse=True):
            try:
                context.append((slugify(contents[0].category),str(contents[0].category).lower()))

            except IndexError:
                pass
        return context

    def sort_languages(self, request, url_name):
        querysets_list = []
        content_queryset = Content.objects.filter(status="approved")
        try:
            name = self.path_info.split("/")[2]
        except IndexError:
            return None
        if url_name == "category":
            category = Category.objects.filter(name=name)[0]
            content_queryset = content_queryset.filter(category=category)
        elif url_name == "topic":
            topic = Topic.objects.filter(name=name)[0]
            content_queryset = content_queryset.filter(topic=topic)
        elif url_name == "language":
            content_queryset = content_queryset.filter(language=name)
        elif url_name == "filter":
            content_queryset = model_filter(request.GET.items(), content_queryset).get("queryset")
        for language in languages:
            querysets = content_queryset.filter(language = language)
            try:
                querysets[0]
            except:
                pass
            else:
                querysets_list.append(querysets)
        context = []
        for contents in sorted(querysets_list, key=len, reverse=True):
            try:
                context.append(
                    (
                        slugify(contents[0].language),
                        str(contents[0].language).lower(),
                        len(contents)
                        )
                    )
            except IndexError:
                pass
        return context

    @staticmethod
    def sort_topics(request):
        contents = Content.objects.filter(status="approved")
        topic_querysets = [
            Content.objects.filter(
                topic = content.topic
            ) for content in contents
        ]
        topics = dict()
        check = []
        for content in sorted(topic_querysets, key=len, reverse=True):
            try:
                topic = Topic.objects.filter(name=content[0].topic, editable=False)[0]
                if len(topics) == 30:
                    break
                elif topic.name not in check:
                    topics.__setitem__(topic, contents.filter(topic=content[0].topic).count())
                    check.append(topic.name)
            except IndexError:
                pass
        return topics
