from django.contrib.sitemaps.views import sitemap
from django.urls import path

from ..views.sitemap import (
    CategorySitemap, CommitSitemap, ContentSitemap, IssueSitemap,
    LanuageSitemap, TopicSitemap, UserSitemap, UtopicSitemap, robots
)

urlpatterns = [
    path("robots.txt/", robots),
    path("sitemap/topic.xml/", sitemap, {"sitemaps": {"topic": TopicSitemap()}}),
    path(
        "sitemap/language.xml/", sitemap, {"sitemaps": {"language": LanuageSitemap()}}
    ),
    path(
        "sitemap/category.xml/", sitemap, {"sitemaps": {"category": CategorySitemap()}}
    ),
    path("sitemap/utopic.xml/", sitemap, {"sitemaps": {"utopic": UtopicSitemap()}}),
    path("sitemap/content.xml/", sitemap, {"sitemaps": {"content": ContentSitemap()}}),
    path("sitemap/user.xml/", sitemap, {"sitemaps": {"user": UserSitemap()}}),
    path("sitemap/issue.xml/", sitemap, {"sitemaps": {"issue": IssueSitemap()}}),
    path("sitemap/commit.xml/", sitemap, {"sitemaps": {"commit": CommitSitemap()}}),
]
