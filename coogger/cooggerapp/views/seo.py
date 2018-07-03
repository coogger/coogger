#django
from django.contrib.sitemaps import Sitemap
from django.shortcuts import render
from django.contrib.auth.models import User

#models
from cooggerapp.models import Content

class TopicSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        topics = []
        items_list = []
        for i in Content.objects.all():
            if i.topic not in topics:
                topics.append(i.topic)
                items_list.append(i)
        return items_list

    def lastmod(self,obj):
        return Content.objects.filter(topic = obj.topic)[0].lastmod

    def location(self,obj):
        return "/"+obj.topic+"/@"+obj.user.username


class ContentSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return Content.objects.all()

    def lastmod(self,obj):
        return obj.lastmod

    def location(self,obj):
        return "/"+obj.get_absolute_url()


class UsersSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return User.objects.all()

    def lastmod(self,obj):
        try:
            return Content.objects.filter(user = obj)[0].time
        except IndexError:
            pass

    def location(self,obj):
        return "/@"+obj.username

def robots(request):
    template = "robots.txt"
    return render(request,template,{})
