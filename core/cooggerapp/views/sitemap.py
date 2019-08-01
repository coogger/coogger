#django
from django.contrib.sitemaps import Sitemap
from django.shortcuts import render
from django.contrib.auth.models import User

#models
from ..models import Content, UTopic, Topic, Category

#choices
from ..choices import LANGUAGES

class TopicSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Topic.objects.all()

    def location(self, obj):
        return "/topic/"+obj.name.lower()


class LanuagesSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return LANGUAGES

    def lastmod(self, obj):
        try:
            contents = Content.objects.filter(language=obj, reply=None)
            return contents[0].last_update
        except IndexError:
            pass

    def location(self, obj):
        return "/language/"+obj


class CategoriesSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        try:
            contents = Content.objects.filter(category=obj, reply=None)
            return contents[0].last_update
        except IndexError:
            pass

    def location(self, obj):
        return "/category/"+obj.name


class UtopicSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return UTopic.objects.all()

    def lastmod(self, obj):
        contents = Content.objects.filter(utopic=obj, reply=None)
        try:
            return contents[0].last_update
        except (AssertionError, IndexError):
            return None

    def location(self, obj):
        return "/"+obj.name+"/@"+obj.user.username


class ContentSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return Content.objects.all()

    def lastmod(self, obj):
        return obj.last_update

    def location(self, obj):
        return obj.get_absolute_url


class UsersSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return User.objects.all()

    def lastmod(self, obj):
        contents = Content.objects.filter(user=obj, status="ready", reply=None)
        try:
            return contents[0].last_update
        except IndexError:
            return None

    def location(self, obj):
        return "/@"+obj.username


def robots(request):
    template = "robots.txt"
    return render(request, template, {})
