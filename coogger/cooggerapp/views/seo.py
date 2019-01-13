# django
from django.contrib.sitemaps import Sitemap
from django.shortcuts import render

# models
from cooggerapp.models import Content


class TopicSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        topics = []
        items_list = []
        for i in Content.objects.filter(status="approved"):
            if i.topic not in topics:
                topics.append(i.topic)
                items_list.append(i)
        return items_list

    def lastmod(self, obj):
        contents = Content.objects.filter(topic=obj.topic, status="approved")
        return contents[int(contents.count()-1)].date

    def location(self, obj):
        return "/"+obj.topic+"/@"+obj.user.username


class ContentSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return Content.objects.filter(status="approved")

    def lastmod(self, obj):
        return obj.date

    def location(self, obj):
        return "/"+obj.get_absolute_url


class UsersSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    # limit = 50

    def items(self):
        return User.objects.all()

    def lastmod(self, obj):
        contents = Content.objects.filter(user=obj)
        try:
            return contents[contents.count()-1].date
        except AssertionError:
            return None

    def location(self, obj):
        return "/@"+obj.username

    # @property
    # def paginator(self):
    # from django.core.paginator import Paginator
    #     return Paginator(self.items(), self.limit)


def robots(request):
    template = "robots.txt"
    return render(request, template, {})
