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
    path("accounts/", include('steemconnect_auth.urls')), # signup, login or create new user
    path("admin/", admin.site.urls), # admin panel
    path("api/", include("core.api.urls")),
    path("post/", include("core.cooggerapp.urls.post")),  # post
    path("delete/", include("core.cooggerapp.urls.delete")),  # delete
    path('privacy/', just_redirect_by_name, name="privacy"),
    path("settings/", include("core.cooggerapp.urls.settings")),
    path("", include("core.cooggerapp.urls.explorer")),  # explorer
    path("", include("core.cooggerapp.urls.home")),  # home
    path("", include("core.cooggerapp.urls.detail")),  # post detail
    path("", include("core.cooggerapp.urls.utopic")),  # user topic
    path("", include("core.cooggerapp.urls.commit")),  # commit pages
    path("", include("core.cooggerapp.urls.issue")),  # issue pages
    path("", include("core.cooggerapp.urls.users")),  # users
    path("", include("core.cooggerapp.urls.sitemap")),  # sitemap
    path("", include("cooggerimages.urls")), # images
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
