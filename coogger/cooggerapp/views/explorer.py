# TODO:  burayı bir güzelliştir

# django
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages as ms
from django.contrib.auth.models import User

# django class based
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
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
            queryset = Content.objects.filter(community=self.request.community_model, tag__contains=hashtag, status="approved")
            info_of_cards = paginator(self.request, queryset)
            context = super(Hashtag, self).get_context_data(**kwargs)
            context["content"] = info_of_cards
            context["nameofhashtag"] = hashtag
            return context


class Userlist(TemplateView):
    template_name = "card/blogs.html"

    def get_context_data(self, list_, **kwargs):
        if list_ != "":
            queryset = Content.objects.filter(community=self.request.community_model, topic__contains=list_, status="approved")
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
            queryset = Content.objects.filter(community=self.request.community_model, language=lang_name, status="approved")
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
            queryset = self.ctof(community=self.request.community_model, category=cat_name, status="approved")
            info_of_cards = paginator(self.request, queryset)
            context = super(Categories, self).get_context_data(**kwargs)
            context["content"] = info_of_cards
            context["category"] = cat_name
            return context


class Filter(TemplateView):
    template_name = "card/blogs.html"
    queryset = Content.objects

    def get_context_data(self, **kwargs):
        for key, value in self.request.GET.items():
            if key == "community":
                community_model = Community.objects.filter(name=value)[0]
                self.queryset = self.queryset.filter(community=community)
            if key == "topic":
                self.queryset = self.queryset.filter(topic=value)
            if key == "category":
                self.queryset = self.queryset.filter(category=value)
            if key == "username":
                user = User.objects.filter(username=value)[0]
                self.queryset = self.queryset.filter(user=user)
            if key == "mod":
                user = User.objects.filter(username=value)[0]
                self.queryset = self.queryset.filter(mod=user)
            if key == "language":
                self.queryset = self.queryset.filter(language=value)
            if key == "permlink":
                self.queryset = self.queryset.filter(permlink=value)
            if key == "status":
                self.queryset = self.queryset.filter(status=value)
        info_of_cards = paginator(self.request, self.queryset)
        context = super(Filter, self).get_context_data(**kwargs)
        context["content"] = info_of_cards
        context["filter"] = True
        return context

#
# defaults = {'first_name': 'Bob'}
# try:
#     obj = Person.objects.get(first_name='John', last_name='Lennon')
#     for key, value in defaults.items():
#         setattr(obj, key, value)
#     obj.save()
# except Person.DoesNotExist:
#     new_values = {'first_name': 'John', 'last_name': 'Lennon'}
#     new_values.update(defaults)
#     obj = Person(**new_values)
#     obj.save()
