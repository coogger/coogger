from django.contrib.auth.models import User
from django.contrib.sitemaps import Sitemap
from django.shortcuts import render
from django.urls import reverse

from ..choices import LANGUAGES
from ..models import Commit, Content, Issue, Topic, UTopic


class IssueSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Issue.objects.filter(utopic__status="public")

    def location(self, obj):
        return reverse(
            "detail-issue",
            kwargs=dict(
                username=str(obj.user),
                utopic_permlink=obj.utopic.permlink,
                issue_id=obj.id,
            ),
        )


class CommitSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Commit.objects.filter(utopic__status="public")

    def location(self, obj):
        return obj.get_absolute_url


class TopicSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Topic.objects.all()

    def location(self, obj):
        return f"/explorer/topic/{obj}/"


class LanuageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return LANGUAGES

    def lastmod(self, obj):
        try:
            contents = Content.objects.filter(language=obj)
            return contents[0].updated
        except IndexError:
            pass

    def location(self, obj):
        return reverse("language", kwargs=dict(language=obj))


class UtopicSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return UTopic.objects.all()

    def lastmod(self, obj):
        contents = Content.objects.filter(utopic=obj)
        try:
            return contents[0].updated
        except (AssertionError, IndexError):
            return None

    def location(self, obj):
        return obj.get_absolute_url


class ContentSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return Content.objects.filter(utopic__status="public")

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return obj.get_absolute_url


class UserSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return User.objects.filter(is_active=True)

    def lastmod(self, obj):
        contents = Content.objects.filter(
            user=obj, status="ready", utopic__status="public"
        )
        try:
            return contents[0].updated
        except IndexError:
            return None

    def location(self, obj):
        return reverse("user", kwargs=dict(username=str(obj)))


def robots(request):
    template = "robots.txt"
    return render(request, template, {})
