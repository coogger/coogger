from django.conf.urls import url

from django.contrib.sitemaps.views import sitemap
#views
from cooggerapp.views import seo

urlpatterns = [
    url(r'^robots.txt/$',seo.robots),
    url(r'^sitemap/topic.xml/$', sitemap, {'sitemaps': {"topic":seo.TopicSitemap()}}),
    url(r'^sitemap/content.xml/$', sitemap, {'sitemaps': {"content":seo.ContentSitemap()}}),
    url(r'^sitemap/users.xml/$', sitemap, {'sitemaps': {"users":seo.UsersSitemap()}}),
    ]
