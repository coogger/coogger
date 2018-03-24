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
from social_django.models import UserSocialAuth

#django class based
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

# cooggerapp models
from apps.cooggerapp.models import Content,UserFollow,Comment,Notification,Contentviews

# cooggerapp views
from apps.cooggerapp.views.tools import (paginator,html_head,hmanynotifications,users_web)
from apps.cooggerapp.views.users import is_follow
from lib.oogg import Oogg

#python
import json
import os
from bs4 import BeautifulSoup

class Detail(TemplateView):
    template_name = "apps/cooggerapp/detail/main_detail.html"
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
        self.up_content_view(queryset) # ip aldık ve okuma sayısını 1 arttırdık
        context = super(Detail, self).get_context_data(**kwargs)
        context["head"] = html_head(queryset)
        context["content_user"] = content_user
        context["nav_category"] = nav_category
        context["urloftopic"] = queryset.url
        context["nameoflist"] = utopic
        context["content"] = info_of_cards
        context["detail"] = queryset
        context["global_hashtag"] = [i for i in queryset.tag.split(" ") if i != ""]
        context["comment_form"] = Comment.objects.filter(content=queryset)
        context["hmanynotifications"] = hmanynotifications(self.request)
        context["user_follow"] = users_web(content_user)
        context["is_follow"] = is_follow(self.request,content_user)
        return context

    def up_content_view(self,queryset):
        Content.objects.filter(id = queryset.id).update(read = F("read")+1)
        try:
            ip = self.request.META["HTTP_X_FORWARDED_FOR"].split(',')[-1].strip()
        except:
            ip = None
        if ip is None:
            return False
        if not Contentviews.objects.filter(content = queryset,ip = ip).exists():
            Contentviews(content = queryset,ip = ip).save()
            queryset.views = F("views") + 1
            queryset.save()


class CommentClassBased(View):

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            request_user = request.user
            comment = request.POST["comment"]
            content_path = request.POST["content_path"]
            if comment:
                content = Content.objects.filter(url = content_path)
                Comment(user = request_user,comment=comment,content = content[0]).save()
                content.update(hmanycomment = F("hmanycomment")+1)
                if str(content[0].user) != str(request_user.username):
                    Notification(user=content[0].user,even = 1,content=comment,address = content_path).save()
                return HttpResponse(json.dumps({"comment": comment,"username":request_user.username}))
            return HttpResponse(None)
