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
        url_name = resolve(request.path_info).url_name
        request.categories = make_choices([category for category in self.sort_categories(request)])
        request.languages = make_choices([language for language in self.sort_languages(request)])
        topics_urls = ["home", "search", "explorer_posts"]
        if url_name in topics_urls:
            request.topics = self.sort_topics(request)
        request.dapps = make_choices([dapp.name for dapp in self.sort_dapps])
        request.settings = settings

    def sort_categories(self, request):
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

    def sort_languages(self, request):
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

    @property
    def sort_dapps(self):
        queryset = Dapp.objects.filter(active=True)
        return queryset

    def sort_topics(self, request):
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
