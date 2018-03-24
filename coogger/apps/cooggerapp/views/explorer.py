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
from apps.cooggerapp.models import Content

#views
from apps.cooggerapp.views.tools import paginator

class Hashtag(TemplateView):
    template_name = "apps/cooggerapp/card/blogs.html"
    ctof = Content.objects.filter
    pagi = 10
    info = "konu etiketi"

    def get_context_data(self, hashtag, **kwargs):
        if hashtag != "":
            queryset = self.ctof(tag__contains = hashtag, confirmation = True)
            info_of_cards = paginator(self.request,queryset,self.pagi)
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

class Userlist(Hashtag):
    template = "apps/cooggerapp/card/blogs.html"
    info = "liste"

    def get_context_data(self, list_, **kwargs):
        if list_ != "":
            queryset = self.ctof(content_list = list_, confirmation = True)
            return super(Userlist, self).get_context_data(list_,**kwargs)
