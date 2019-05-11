# django
from django.urls import include, path, resolve
from django.contrib import admin
from django.shortcuts import render

# django.conf
from django.conf import settings
from django.conf.urls.static import static


def just_redirect(request):
    "No ads due to adblock=True"
    url_name = resolve(request.path_info).url_name
    template_name = f"{url_name}.html"
    return render(request, template_name, dict(adblock=True))

# common addresses
urlpatterns = [
    path("accounts/", include('steemconnect_auth.urls')), # signup, login or create new user
    path("admin/", admin.site.urls), # admin panel
    path("api/", include("core.api.urls")),
    path("post/", include("core.cooggerapp.urls.post")),  # post
    path("delete/", include("core.cooggerapp.urls.delete")),  # delete
    path('adblock/', just_redirect, name="adblock"), # if user use adblock
    path('privacy/', just_redirect, name="privacy"),
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
