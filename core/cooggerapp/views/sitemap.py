from django.contrib.auth.models import User
from django.contrib.sitemaps import Sitemap
from django.shortcuts import render
from django.urls import reverse

from ..choices import LANGUAGES
from ..models import Category, Commit, Content, Issue, Topic, UTopic


class IssueSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Issue.objects.all()

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
        return Commit.objects.all()

    def location(self, obj):
        return reverse(
            "commit",
            kwargs=dict(
                username=str(obj.user),
                topic_permlink=obj.utopic.permlink,
                hash=obj.hash,
            ),
        )


class TopicSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Topic.objects.all()

    def location(self, obj):
        return reverse("topic", kwargs=dict(permlink=obj.permlink))


class LanuageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return LANGUAGES

    def lastmod(self, obj):
        try:
            contents = Content.objects.filter(language=obj)
            return contents[0].last_update
        except IndexError:
            pass

    def location(self, obj):
        return reverse("language", kwargs=dict(lang_name=obj))


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        try:
            contents = Content.objects.filter(category=obj)
            return contents[0].last_update
        except IndexError:
            pass

    def location(self, obj):
        return reverse("category", kwargs=dict(cat_name=obj.name))


class UtopicSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return UTopic.objects.all()

    def lastmod(self, obj):
        contents = Content.objects.filter(utopic=obj)
        try:
            return contents[0].last_update
        except (AssertionError, IndexError):
            return None

    def location(self, obj):
        return reverse(
            "detail-utopic", kwargs=dict(permlink=obj.permlink, username=str(obj.user))
        )


class ContentSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return Content.objects.all()

    def lastmod(self, obj):
        return obj.last_update

    def location(self, obj):
        return obj.get_absolute_url


class UserSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return User.objects.all()

    def lastmod(self, obj):
        contents = Content.objects.filter(user=obj, status="ready")
        try:
            return contents[0].last_update
        except IndexError:
            return None

    def location(self, obj):
        return reverse("user", kwargs=dict(username=str(obj)))


def robots(request):
    template = "robots.txt"
    return render(request, template, {})
