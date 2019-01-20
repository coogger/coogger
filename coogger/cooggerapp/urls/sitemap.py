from django.conf.urls import url

from django.contrib.sitemaps.views import sitemap
# views
from cooggerapp.views.sitemap import (
    TopicSitemap, UtopicSitemap,
    ContentSitemap, UsersSitemap,
    robots, LanuagesSitemap, CategoriesSitemap
)

urlpatterns = [
    url(r'^robots.txt/$', robots),
    url(r'^sitemap/topic.xml/$', sitemap, {'sitemaps': {"topic": TopicSitemap()}}),
    url(r'^sitemap/languages.xml/$', sitemap, {'sitemaps': {"languages": LanuagesSitemap()}}),
    url(r'^sitemap/category.xml/$', sitemap, {'sitemaps': {"category": CategoriesSitemap()}}),
    url(r'^sitemap/utopic.xml/$', sitemap, {'sitemaps': {"utopic": UtopicSitemap()}}),
    url(r'^sitemap/content.xml/$', sitemap, {'sitemaps': {"content": ContentSitemap()}}),
    url(r'^sitemap/users.xml/$', sitemap, {'sitemaps': {"users": UsersSitemap()}}),
    ]
