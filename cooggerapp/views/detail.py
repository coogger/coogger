#django
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import F
from django.contrib import messages as ms
from django.utils.text import slugify
from django.utils import timezone

#django class based
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

#models
from cooggerapp.models import Content,Contentviews,UserFollow,Comment,Notification

#views
from cooggerapp.views.tools import (paginator,html_head,hmanynotifications,users_web,is_user_author)
from cooggerapp.views.users import is_follow

#python
import json
import os
from bs4 import BeautifulSoup

class DetailBasedClass(TemplateView):
    template_name = "detail/main_detail.html"
    ctof = Content.objects.filter
    pagi = 6

    def get_context_data(self,username,utopic,path, **kwargs):
        content_path = username+"/"+utopic+"/"+path
        if username == self.request.user.username:
            queryset = self.ctof(url = content_path)[0]
        else:
            queryset = self.ctof(url = content_path, confirmation = True)[0]
        content_user = queryset.user
        queryset = self.ctof(url = content_path)[0]
        content_id = queryset.id
        nav_category = self.ctof(user = content_user,content_list = utopic)
        info_of_cards = paginator(self.request,nav_category,self.pagi)
        ip = self.get_ip(self.request)
        if ip is not None: # ip adres alma başarılı ise
            self.up_content_view(queryset,ip) # okuma sayısını 1 arttırdık
        context = super(DetailBasedClass, self).get_context_data(**kwargs)
        context["head"] = html_head(queryset)
        context["content_user"] = content_user
        context["nav_category"] = nav_category
        context["nameoftopic"] = queryset.title
        context["nameoflist"] = utopic
        context["content"] = info_of_cards
        context["detail"] = queryset
        context["global_hashtag"] = [i for i in queryset.tag.split(",") if i != ""]
        context["comment_form"] = Comment.objects.filter(content=queryset)
        context["hmanynotifications"] = hmanynotifications(self.request)
        context["user_follow"] = users_web(content_user)
        context["is_follow"] = is_follow(self.request,content_user)
        return context

    @staticmethod
    def get_ip(request):
        try:
            ip = request.META["HTTP_X_FORWARDED_FOR"].split(',')[-1].strip()
        except:
            return None
        return ip

    @staticmethod
    def up_content_view(queryset,ip):
        if not Contentviews.objects.filter(content = queryset,ip = ip).exists():
            Contentviews(content = queryset,ip = ip).save()
            queryset.views = F("views") + 1
            queryset.save()

class CommentBasedClass(View):

    @method_decorator(login_required)
    def post(self, request,content_path, *args, **kwargs):
        if request.is_ajax():
            user = request.user
            comment = request.POST["comment"]
            if comment:
                content = Content.objects.filter(url = content_path)[0]
                Comment(user=user,comment=comment,content = content).save()
                content.hmanycomment = F("hmanycomment")+1
                content.save()
                if str(content.user) != str(user.username):
                    Notification(user=content.user,even = 1,content=comment,address = content_path).save()
                return HttpResponse(json.dumps({"comment": comment,"username":request.user.username}))
            return HttpResponse(None)
