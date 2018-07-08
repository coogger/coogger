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
from cooggerapp.views.tools import paginator,get_community_model

class Hashtag(TemplateView):
    template_name = "card/blogs.html"

    def get_context_data(self, hashtag, **kwargs):
        if hashtag != "":
            community_model = get_community_model(self.request)
            queryset = Content.objects.filter(community = community_model,tag__contains = hashtag,status = "approved")
            info_of_cards = paginator(self.request,queryset)
            context = super(Hashtag, self).get_context_data(**kwargs)
            html_head = dict(
             title = hashtag,
             keywords = hashtag,
             description = hashtag,
            )
            context["content"] = info_of_cards
            context["nameofhashtag"] = hashtag
            context["head"] = html_head
            context["community"] = community_model
            return context

class Userlist(TemplateView):
    template_name = "card/blogs.html"

    def get_context_data(self, list_, **kwargs):
        if list_ != "":
            community_model = get_community_model(self.request)
            queryset = Content.objects.filter(community = community_model,topic__contains = list_,status = "approved")
            info_of_cards = paginator(self.request,queryset)
            context = super(Userlist, self).get_context_data(**kwargs)
            html_head = dict(
             title = list_,
             keywords = list_,
             description = list_,
            )
            context["content"] = info_of_cards
            context["nameofhashtag"] = list_
            context["head"] = html_head
            context["community"] = community_model
            return context

class LeftSide(TemplateView): # TODO:  do language check,  is it necessary ?
    template_name = "card/blogs.html"

    def get_context_data(self, left, **kwargs):
        if left != "":
            community_model = get_community_model(self.request)
            queryset = Content.objects.filter(community = community_model,left_side = left,status = "approved")
            info_of_cards = paginator(self.request,queryset)
            context = super(Language, self).get_context_data(**kwargs)
            html_head = dict(
             title = left,
             keywords = left,
             description = left,
            )
            context["content"] = info_of_cards
            context["language"] = lang
            context["head"] = html_head
            context["community"] = community_model
            return context

class RightSide(TemplateView):
    template_name = "card/blogs.html"
    ctof = Content.objects.filter

    def get_context_data(self, right, **kwargs):
        if right != "":
            community_model = get_community_model(self.request)
            queryset = self.ctof(community = community_model,right_side = right,status = "approved")
            info_of_cards = paginator(self.request,queryset)
            context = super(Category, self).get_context_data(**kwargs)
            html_head = dict(
             title = right,
             keywords = right,
             description = right,
            )
            context["content"] = info_of_cards
            context["category"] = right
            context["head"] = html_head
            context["community"] = community_model
            return context

class Filter(TemplateView):
    template_name = "card/blogs.html"
    queryset = Content.objects

    def get_context_data(self, **kwargs):
        for key,value in self.request.GET.items():
            if key == "community":
                community = Community.objects.filter(name = value)[0]
                self.queryset = self.queryset.filter(community = community)
            if key == "topic":
                self.queryset = self.queryset.filter(topic = value)
            if key == "right_side":
                self.queryset = self.queryset.filter(right_side = value)
            if key == "username":
                user = User.objects.filter(username = value)[0]
                self.queryset = self.queryset.filter(user = user)
            if key == "mod":
                user = User.objects.filter(username = value)[0]
                self.queryset = self.queryset.filter(mod = user)
            if key == "left_side":
                self.queryset = self.queryset.filter(left_side = value)
            if key == "permlink":
                self.queryset = self.queryset.filter(permlink = value)
            if key == "status":
                self.queryset = self.queryset.filter(status = value)
        info_of_cards = paginator(self.request,self.queryset)
        context = super(Filter, self).get_context_data(**kwargs)
        html_head = dict(
         title = "filter",
         description = "",
        )
        context["content"] = info_of_cards
        context["filter"] = True
        context["head"] = html_head
        context["community"] = community_model
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
