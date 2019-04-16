# django
from django.urls import path, include
from django.shortcuts import render
from django.urls import resolve

# views
from core.cooggerapp.views import (csettings)

# main project = coogger

def just_redirect(request):
    "No ads due to adblock=True"
    url_name = resolve(request.path_info).url_name
    template_name = f"{url_name}.html"
    return render(request, template_name, dict(adblock=True))

urlpatterns = [
    path("post/", include("core.cooggerapp.urls.post")),  # post
    path("settings", csettings.Settings.as_view(), name="settings"),
    path("delete", include("core.cooggerapp.urls.delete")),  # delete
    path("", include("core.cooggerapp.urls.explorer")),  # explorer
    path("", include("core.cooggerapp.urls.home")),  # home
    path("", include("core.cooggerapp.urls.detail")),  # post detail
    path("", include("core.cooggerapp.urls.users")),  # users
    path("", include("core.cooggerapp.urls.sitemap")),  # sitemap
    path('adblock/', just_redirect, name="adblock"),
    path('privacy/', just_redirect, name="privacy"),
]
