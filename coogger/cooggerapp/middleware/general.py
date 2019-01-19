from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.urls import resolve

# models.
from cooggerapp.models import CategoryofDapp, Content, Topic
from steemconnect_auth.models import Dapp

# coices
from cooggerapp.choices import *

class GeneralMiddleware(MiddlewareMixin):

    def process_request(self, request):
        self.path_info = request.path_info
        if self.path_info.split("/")[1] == "api":
            return None
        url_name = resolve(self.path_info).url_name
        request.categories = make_choices([category for category in self.sort_categories(request)])
        request.languages = make_choices([language for language in self.sort_languages(request)])
        topics_urls = ["home", "search", "explorer_posts"]
        if url_name in topics_urls:
            request.topics = self.sort_topics(request)
        request.dapps = make_choices([dapp.name for dapp in self.sort_dapps()])
        request.settings = settings

    @staticmethod
    def sort_categories(request):
        if request.dapp_model.name == "coogger":
            category_filter = CategoryofDapp.objects.all()
        else:
            category_filter = CategoryofDapp.objects.filter(dapp=request.dapp_model)
        querysets_list = []
        for category in category_filter:
            querysets = Content.objects.filter(category = category.category_name, status="approved")
            querysets_list.append(querysets)
        categories = []
        for contents in sorted(querysets_list, key=len, reverse=True):
            try:
                categories.append(contents[0].category)
            except IndexError:
                pass
        return categories

    @staticmethod
    def sort_languages(request):
        querysets_list = []
        for language in languages:
            querysets = Content.objects.filter(language = language, status="approved")
            querysets_list.append(querysets)
        languages_list = []
        for contents in sorted(querysets_list, key=len, reverse=True):
            try:
                languages_list.append(contents[0].language)
            except IndexError:
                pass
        return languages_list

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
