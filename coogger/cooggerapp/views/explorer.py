# TODO:  burayı bir güzelliştir

# django
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages as ms
from django.contrib.auth.models import User
from django.http import Http404

# django class based
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic.base import TemplateView

# models
from cooggerapp.models import Content, Topic
from steemconnect_auth.models import Dapp, CategoryofDapp

# views
from cooggerapp.views.tools import paginator

# choices
from cooggerapp.choices import languages


class TopicView(TemplateView):
    template_name = "topic/index.html"

    def get_context_data(self, topic, *args, **kwargs):
        queryset = Content.objects.filter(topic=topic, status="approved")
        if queryset.exists():
            if not self.request.dapp_model.name == "coogger":
                queryset = Content.objects.filter(dapp=self.request.dapp_model, topic=topic, status="approved")
            info_of_cards = paginator(self.request, queryset)
            context = super(TopicView, self).get_context_data(**kwargs)
            context["content"] = info_of_cards
            topic_query = Topic.objects.filter(name=topic)
            if topic_query.exists():
                context["topic"] = topic_query[0]
            else:
                Topic(name=topic).save()
            return context
        raise Http404


class Hashtag(TemplateView):
    template_name = "card/blogs.html"

    def get_context_data(self, hashtag, **kwargs):
        queryset = Content.objects.filter(tag__contains=hashtag, status="approved")
        if queryset.exists():
            if not self.request.dapp_model.name == "coogger":
                queryset = queryset.filter(dapp=self.request.dapp_model)
            info_of_cards = paginator(self.request, queryset)
            context = super(Hashtag, self).get_context_data(**kwargs)
            context["content"] = info_of_cards
            context["nameofhashtag"] = hashtag
            return context
        raise Http404


class Languages(TemplateView):
    template_name = "card/blogs.html"

    def get_context_data(self, lang_name, **kwargs):
        if lang_name in languages:
            if self.request.dapp_model.name == "coogger":
                queryset = Content.objects.filter(language=lang_name, status="approved")
            else:
                queryset = Content.objects.filter(dapp=self.request.dapp_model, language=lang_name, status="approved")
            info_of_cards = paginator(self.request, queryset)
            context = super(Languages, self).get_context_data(**kwargs)
            context["content"] = info_of_cards
            context["language"] = lang_name
            return context
        raise Http404


class Categories(TemplateView):
    template_name = "card/blogs.html"
    ctof = Content.objects.filter

    def get_context_data(self, cat_name, **kwargs):
        if CategoryofDapp.objects.filter(category_name=cat_name).exists():
            if self.request.dapp_model.name == "coogger":
                queryset = self.ctof(category=cat_name, status="approved")
            else:
                queryset = self.ctof(dapp=self.request.dapp_model, category=cat_name, status="approved")
            context = super(Categories, self).get_context_data(**kwargs)
            info_of_cards = paginator(self.request, queryset)
            context["content"] = info_of_cards
            context["category"] = cat_name
            return context
        raise Http404


class Filter(TemplateView):
    template_name = "card/blogs.html"
    queryset = Content.objects.filter(status="approved")

    def get_context_data(self, **kwargs):
        filter = ""
        for attr, value in self.request.GET.items():
            if attr and value:
                filter += f"&{attr}={value}"
                if attr == "username":
                    value = User.objects.filter(username=value)[0]
                    attr = "user"
                elif attr == "dapp":
                    value = Dapp.objects.filter(name=value)[0]
                if attr == "tag":
                    try:
                        self.queryset = self.queryset.filter(tag__contains = value)
                    except FieldError:
                        pass
                else:
                    try:
                        self.queryset = self.queryset.filter(**{attr: value})
                    except FieldError:
                        pass
        context = super(Filter, self).get_context_data(**kwargs)
        context["content"] = paginator(self.request, self.queryset)
        context["filter"] = filter
        return context
