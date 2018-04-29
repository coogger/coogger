from django.conf.urls import url

from django.contrib.sitemaps.views import sitemap
#views
from cooggerapp.views import seo

urlpatterns = [
    url(r'^robots.txt/$',seo.robots),
    url(r'^sitemap/cooggerapp/contentlist\.xml/$', sitemap, {'sitemaps': {"content_list":seo.ContentlistSitemap()}}),
    url(r'^sitemap/cooggerapp/content\.xml/$', sitemap, {'sitemaps': {"content":seo.ContentSitemap()}}),
    url(r'^sitemap/cooggerapp/users\.xml/$', sitemap, {'sitemaps': {"users":seo.UsersSitemap()}}),
    ]
