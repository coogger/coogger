# TODO:  burayı bir güzelliştir

# django
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages as ms
from django.contrib.auth.models import User

# django class based
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic.base import TemplateView

# models
from cooggerapp.models import Content

# views
from cooggerapp.views.tools import paginator


class Hashtag(TemplateView):
    template_name = "card/blogs.html"

    def get_context_data(self, hashtag, **kwargs):
        if hashtag != "":
            if self.request.dapp_model.name == "coogger":
                queryset = Content.objects.filter(tag__contains=hashtag, status="approved")
            else:
                queryset = Content.objects.filter(dapp=self.request.dapp_model, tag__contains=hashtag, status="approved")
            info_of_cards = paginator(self.request, queryset)
            context = super(Hashtag, self).get_context_data(**kwargs)
            context["content"] = info_of_cards
            context["nameofhashtag"] = hashtag
            return context


class Userlist(TemplateView):
    template_name = "card/blogs.html"

    def get_context_data(self, list_, **kwargs):
        if list_ != "":
            if self.request.dapp_model.name == "coogger":
                queryset = Content.objects.filter(topic=list_, status="approved")
            else:
                queryset = Content.objects.filter(dapp=self.request.dapp_model, topic=list_, status="approved")
            info_of_cards = paginator(self.request, queryset)
            context = super(Userlist, self).get_context_data(**kwargs)
            context["content"] = info_of_cards
            context["nameofhashtag"] = list_
            return context


class Languages(TemplateView):
    # TODO:  do language check,  is it necessary ?
    template_name = "card/blogs.html"

    def get_context_data(self, lang_name, **kwargs):
        if lang_name != "":
            if self.request.dapp_model.name == "coogger":
                queryset = Content.objects.filter(language=lang_name, status="approved")
            else:
                queryset = Content.objects.filter(dapp=self.request.dapp_model, language=lang_name, status="approved")
            info_of_cards = paginator(self.request, queryset)
            context = super(Languages, self).get_context_data(**kwargs)
            context["content"] = info_of_cards
            context["language"] = lang_name
            return context


class Categories(TemplateView):
    template_name = "card/blogs.html"
    ctof = Content.objects.filter

    def get_context_data(self, cat_name, **kwargs):
        if cat_name != "":
            if self.request.dapp_model.name == "coogger":
                queryset = self.ctof(category=cat_name, status="approved")
            else:
                queryset = self.ctof(dapp=self.request.dapp_model, category=cat_name, status="approved")
            info_of_cards = paginator(self.request, queryset)
            context = super(Categories, self).get_context_data(**kwargs)
            context["content"] = info_of_cards
            context["category"] = cat_name
            return context


class Filter(TemplateView):
    template_name = "card/blogs.html"
    queryset = Content.objects

    def get_context_data(self, **kwargs):
        filter_ = ""
        for attr, value in self.request.GET.items():
            filter_ += f"&{attr}={value}"
            if attr == "username":
                value = User.objects.filter(username=value)[0]
                attr = "user"
            try:
                self.queryset = self.queryset.filter(**{attr: value})
            except FieldError:
                pass
        info_of_cards = paginator(self.request, self.queryset)
        context = super(Filter, self).get_context_data(**kwargs)
        context["content"] = info_of_cards
        print(filter_)
        context["filter"] = filter_
        return context
