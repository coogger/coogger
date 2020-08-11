from django.contrib.sitemaps.views import sitemap
from django.urls import path

from ..views.sitemap import (
    CommitSitemap,
    ContentSitemap,
    IssueSitemap,
    LanuageSitemap,
    TopicSitemap,
    UserSitemap,
    UtopicSitemap,
)

urlpatterns = [
    path("topic.xml/", sitemap, {"sitemaps": {"topic": TopicSitemap()}}),
    path(
        "language.xml/", sitemap, {"sitemaps": {"language": LanuageSitemap()}}
    ),
    path("utopic.xml/", sitemap, {"sitemaps": {"utopic": UtopicSitemap()}}),
    path("content.xml/", sitemap, {"sitemaps": {"content": ContentSitemap()}}),
    path("user.xml/", sitemap, {"sitemaps": {"user": UserSitemap()}}),
    path("issue.xml/", sitemap, {"sitemaps": {"issue": IssueSitemap()}}),
    path("commit.xml/", sitemap, {"sitemaps": {"commit": CommitSitemap()}}),
]
