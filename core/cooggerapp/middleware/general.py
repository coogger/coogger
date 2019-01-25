from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.urls import resolve
from django.utils.text import slugify

# models.
from core.cooggerapp.models import CategoryofDapp, Content, Topic
from core.steemconnect_auth.models import Dapp

# coices
from core.cooggerapp.choices import *


class GeneralMiddleware(MiddlewareMixin):

    def process_request(self, request):
        self.path_info = request.path_info
        invalid = ["sitemap", "api", "robots.txt"]
        if self.path_info.split("/")[1] in invalid:
            return None
        url_name = resolve(self.path_info).url_name
        request.sort_categories = self.sort_categories(request, url_name)
        request.sort_languages = self.sort_languages(url_name)
        topics_urls = ["home", "search", "explorer_posts"]
        if url_name in topics_urls:
            request.topics = self.sort_topics(request)
        request.dapps = make_choices([dapp.name for dapp in self.sort_dapps()])
        request.settings = settings

    def sort_categories(self, request, url_name):
        category_queryset = CategoryofDapp.objects.all()
        if request.dapp_model.name != "coogger":
            category_queryset = category_queryset.filter(
                dapp=request.dapp_model
            )
        querysets_list = []
        content_queryset = Content.objects.filter(status="approved")
        specific_url_names = ["topic", "category"]
        if url_name in specific_url_names:
            name = self.path_info.split("/")[2]
            # /topic/autocad/ = autocad
            # /category/tutorial/ = tutorial
            content_queryset = content_queryset.filter(**{url_name:name})
        for category in category_queryset:
            querysets = content_queryset.filter(category=category.name)
            try:
                querysets[0]
            except:
                pass
            else:
                querysets_list.append(querysets)
        categories = []
        for contents in sorted(querysets_list, key=len, reverse=True):
            try:
                categories.append(
                    dict(
                        name=contents[0].category,
                        count=len(contents),
                    )
                )
            except IndexError:
                pass
        context = []
        for cat in categories:
            name = cat["name"]
            count = cat["count"]
            context.append(
                (
                    slugify(name),
                    str(name).lower(),
                    count
                    )
                )
        return context

    def sort_languages(self, url_name):
        querysets_list = []
        content_queryset = Content.objects.filter(status="approved")
        if url_name == "topic" or url_name == "category":
            name = self.path_info.split("/")[2]
            # /topic/autocad/ = autocad
            # /category/tutorial/ = tutorial
            content_queryset = content_queryset.filter(**{url_name:name})
        for language in languages:
            querysets = content_queryset.filter(language = language)
            try:
                querysets[0]
            except:
                pass
            else:
                querysets_list.append(querysets)
        languages_list = []
        for contents in sorted(querysets_list, key=len, reverse=True):
            try:
                languages_list.append(
                    dict(
                        name=contents[0].language,
                        count=len(contents)
                        )
                    )
            except IndexError:
                pass
        context = []
        for lang in languages_list:
            name = lang["name"]
            count = lang["count"]
            context.append(
                (
                    slugify(name),
                    str(name).lower(),
                    count
                    )
                )
        return context

    @staticmethod
    def sort_dapps():
        queryset = Dapp.objects.filter(active=True)
        return queryset

    @staticmethod
    def sort_topics(request):
        if request.dapp_model.name == "coogger":
            contents = Content.objects.filter(status="approved")
        else:
            contents = Content.objects.filter(
                dapp=request.dapp_model, status="approved"
            )
        topic_querysets = [
            Content.objects.filter(
                topic = content.topic,
                status="approved"
            ) for content in contents
        ]
        topics = []
        check = []
        for content in sorted(topic_querysets, key=len, reverse=True):
            try:
                topic = Topic.objects.filter(name=content[0].topic)[0]
                if len(topics) == 30:
                    break
                elif topic.name not in check:
                    topics.append(topic)
                    check.append(topic.name)
            except IndexError:
                pass
        return topics
