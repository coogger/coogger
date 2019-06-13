# django
from django.urls import include, path, resolve
from django.contrib import admin
from django.shortcuts import render

# django.conf
from django.conf import settings
from django.conf.urls.static import static

# utils
from .utils import just_redirect_by_name

# common addresses
urlpatterns = [
    path("accounts/github/", include('github_auth.urls')),
    path("follow/", include("django_follow_system.urls")),
    path("vote/", include("django_vote_system.urls")),
    path("bookmark/", include("django_bookmark.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("core.api.urls")),
    path("post/", include("core.cooggerapp.urls.post")),
    path("delete/", include("core.cooggerapp.urls.delete")),
    path('privacy/', just_redirect_by_name, name="privacy"),
    path("settings/", include("core.cooggerapp.urls.settings")),
    path("", include("core.cooggerapp.urls.explorer")),
    path("", include("core.cooggerapp.urls.home")),
    path("", include("core.cooggerapp.urls.detail")),
    path("", include("core.cooggerapp.urls.utopic")),
    path("", include("core.cooggerapp.urls.commit")),
    path("", include("core.cooggerapp.urls.issue")),
    path("", include("core.cooggerapp.urls.users")),
    path("", include("core.cooggerapp.urls.sitemap")),
    path("", include("cooggerimages.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
