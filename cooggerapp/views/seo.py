from django.contrib.sitemaps import Sitemap
from django.shortcuts import render
from cooggerapp.models import Content,ContentList
from django.contrib.auth.models import User

class ContentlistSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return ContentList.objects.all()

    def lastmod(self,obj):
        return Content.objects.filter(user = obj.user)[0].time

    def location(self,obj):
        return "/@"+str(obj.user)+"/"+str(obj.content_list)


class ContentSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return Content.objects.all()

    def lastmod(self,obj):
        return obj.lastmod

    def location(self,obj):
        return "/"+obj.url


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
