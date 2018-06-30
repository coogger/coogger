#django
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages as ms
from django.contrib.auth.models import User

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
            queryset = self.ctof(topic__contains = list_,status = "approved")
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
            queryset = self.ctof(category = cat,status = "approved")
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

class Filter(TemplateView):
    template_name = "card/blogs.html"
    info = "Filter"
    queryset = Content.objects

    def get_context_data(self, **kwargs):
        for key,value in self.request.GET.items():
            if key == "topic":
                self.queryset = self.queryset.filter(topic = value)
            if key == "category":
                self.queryset = self.queryset.filter(category = value)
            if key == "username":
                user = User.objects.filter(username = value)[0]
                print(user)
                self.queryset = self.queryset.filter(user = user)
            if key == "mod":
                user = User.objects.filter(username = value)[0]
                self.queryset = self.queryset.filter(mod = user)
            if key == "language":
                self.queryset = self.queryset.filter(language = value)
            if key == "permlink":
                self.queryset = self.queryset.filter(permlink = value)
            if key == "status":
                self.queryset = self.queryset.filter(status = value)
        info_of_cards = paginator(self.request,self.queryset)
        context = super(Filter, self).get_context_data(**kwargs)
        html_head = dict(
         title = "filter | coogger",
         description = " {} altında ki bütün coogger bilgileri".format(self.info),
        )
        context["content"] = info_of_cards
        context["filter"] = True
        context["head"] = html_head
        return context
