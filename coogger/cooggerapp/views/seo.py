#django
from django.contrib.sitemaps import Sitemap
from django.shortcuts import render
from django.contrib.auth.models import User

#models
from cooggerapp.models import Content

class ContentlistSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return [i for i in Content.objects.filter(status = "approved")]

    def lastmod(self,obj):
        return Content.objects.filter(content_list = obj.content_list,status = "approved")[0].lastmod

    def location(self,obj):
        return "/"+obj.get_absolute_url


class ContentSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return Content.objects.filter(status = "approved")

    def lastmod(self,obj):
        return obj.lastmod

    def location(self,obj):
        return "/@"+obj.url


class UsersSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return User.objects.all()

    def lastmod(self,obj):
        try:
            return Content.objects.filter(user = obj,status = "approved")[0].time
        except IndexError:
            pass

    def location(self,obj):
        return "/@"+obj.username

def robots(request):
    template = "robots.txt"
    return render(request,template,{})
