# TODO topic -> utopic etc

# django
from django.contrib.sitemaps import Sitemap
from django.shortcuts import render
from django.contrib.auth.models import User

# models
from core.cooggerapp.models import Content, Topic, Category

# choices
from core.cooggerapp.choices import LANGUAGES

class TopicSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Topic.objects.all()

    def lastmod(self, obj):
        try:
            contents = Content.objects.filter(topic=obj, status="approved", reply=None)
            return contents[0].last_update
        except IndexError:
            pass

    def location(self, obj):
        return "/topic/"+obj.name


class LanuagesSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return LANGUAGES

    def lastmod(self, obj):
        try:
            contents = Content.objects.filter(language=obj, status="approved", reply=None)
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
            contents = Content.objects.filter(category=obj.name, status="approved", reply=None)
            return contents[0].last_update
        except IndexError:
            pass

    def location(self, obj):
        return "/category/"+obj.name


class UtopicSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        topics = []
        items_list = []
        for i in Content.objects.filter(status="approved", reply=None):
            if i.topic not in topics:
                topics.append(i.topic)
                items_list.append(i)
        return items_list

    def lastmod(self, obj):
        contents = Content.objects.filter(topic=obj.topic, status="approved", reply=None)
        return contents[int(contents.count()-1)].last_update

    def location(self, obj):
        return "/"+obj.topic.name+"/@"+obj.user.username


class ContentSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return Content.objects.filter(status="approved", reply=None)

    def lastmod(self, obj):
        return obj.last_update

    def location(self, obj):
        return "/"+obj.get_absolute_url


class UsersSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return SteemConnectUser.objects.all()

    def lastmod(self, obj):
        contents = Content.objects.filter(user=obj.user, status="approved", reply=None)
        try:
            return contents[contents.count()-1].last_update
        except AssertionError:
            return None

    def location(self, obj):
        return "/@"+obj.username


def robots(request):
    template = "robots.txt"
    return render(request, template, {})
