#django
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages as ms

#django class based
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.base import TemplateView

#models
from cooggerapp.models import Content

#views
from cooggerapp.views.tools import paginator

class Hashtag(TemplateView):
    template_name = "card/blogs.html"
    ctof = Content.objects.filter
    info = "Hashtag"

    def get_context_data(self, hashtag, **kwargs):
        if hashtag != "":
            queryset = self.ctof(tag__contains = hashtag,status = "approved")
            info_of_cards = paginator(self.request,queryset)
            context = super(Hashtag, self).get_context_data(**kwargs)
            html_head = dict(
             title = hashtag+" | coogger",
             keywords = hashtag,
             description = hashtag +" {} altında ki bütün coogger bilgileri".format(self.info),
            )
            context["content"] = info_of_cards
            context["nameofhashtag"] = hashtag
            context["head"] = html_head
            return context

class Userlist(TemplateView):
    template_name = "card/blogs.html"
    info = "List"
    ctof = Content.objects.filter

    def get_context_data(self, list_, **kwargs):
        if list_ != "":
            queryset = self.ctof(content_list__contains = list_,status = "approved")
            info_of_cards = paginator(self.request,queryset)
            context = super(Userlist, self).get_context_data(**kwargs)
            html_head = dict(
             title = list_+" | coogger",
             keywords = list_,
             description = list_ +" {} altında ki bütün coogger bilgileri".format(self.info),
            )
            context["content"] = info_of_cards
            context["nameofhashtag"] = list_
            context["head"] = html_head
            return context

class Language(TemplateView): # TODO:  do language check,  is it necessary ?
    template_name = "card/blogs.html"
    info = "Language"
    ctof = Content.objects.filter

    def get_context_data(self, lang, **kwargs):
        if lang != "":
            queryset = self.ctof(language = lang,status = "approved")
            info_of_cards = paginator(self.request,queryset)
            context = super(Language, self).get_context_data(**kwargs)
            html_head = dict(
             title = lang+" | coogger",
             keywords = lang,
             description = lang +" {} altında ki bütün coogger bilgileri".format(self.info),
            )
            context["content"] = info_of_cards
            context["language"] = lang
            context["head"] = html_head
            return context

class Category(TemplateView): # TODO:  do Category check,  is it necessary ?
    template_name = "card/blogs.html"
    info = "Category"
    ctof = Content.objects.filter

    def get_context_data(self, cat, **kwargs):
        if cat != "":
            queryset = self.ctof(type = cat,status = "approved")
            info_of_cards = paginator(self.request,queryset)
            context = super(Category, self).get_context_data(**kwargs)
            html_head = dict(
             title = cat+" | coogger",
             keywords = cat,
             description = cat +" {} altında ki bütün coogger bilgileri".format(self.info),
            )
            context["content"] = info_of_cards
            context["category"] = cat
            context["head"] = html_head
            return context
