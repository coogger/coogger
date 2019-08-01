# django
from django.urls import path
from django.contrib.sitemaps.views import sitemap

# views
from ..views.sitemap import (
    TopicSitemap,
    UtopicSitemap,
    ContentSitemap,
    UsersSitemap,
    robots,
    LanuagesSitemap,
    CategoriesSitemap,
)

urlpatterns = [
    path("robots.txt/", robots),
    path("sitemap/topic.xml/", sitemap, {"sitemaps": {"topic": TopicSitemap()}}),
    path(
        "sitemap/languages.xml/",
        sitemap,
        {"sitemaps": {"languages": LanuagesSitemap()}},
    ),
    path(
        "sitemap/category.xml/",
        sitemap,
        {"sitemaps": {"category": CategoriesSitemap()}},
    ),
    path("sitemap/utopic.xml/", sitemap, {"sitemaps": {"utopic": UtopicSitemap()}}),
    path("sitemap/content.xml/", sitemap, {"sitemaps": {"content": ContentSitemap()}}),
    path("sitemap/users.xml/", sitemap, {"sitemaps": {"users": UsersSitemap()}}),
]
