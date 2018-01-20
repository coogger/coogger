#django
from django.contrib.sitemaps import Sitemap
from django.shortcuts import render
from django.contrib.auth.models import User

#models
from cooggerapp.models import Content,ContentList

class ContentlistSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return ContentList.objects.all()

    def lastmod(self,obj):
        return Content.objects.filter(user = obj.user, confirmation = True)[0].time

    def location(self,obj):
        return "/"+str(obj.user)+"/"+str(obj.content_list)


class ContentSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return Content.objects.filter(confirmation = True)

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
            return Content.objects.filter(user = obj, confirmation = True)[0].time
        except IndexError:
            pass

    def location(self,obj):
        return "/"+obj.username

def robots(request):
    template = "robots.txt"
    return render(request,template,{})
