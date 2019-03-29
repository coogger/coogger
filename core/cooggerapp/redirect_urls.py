# django
from django.urls import path, include

# views
from core.cooggerapp.views import (csettings)

# main project = coogger
urlpatterns = [
    path("post/", include("core.cooggerapp.urls.post")),  # post
    path("settings", csettings.Settings.as_view(), name="settings"),
    path("delete", include("core.cooggerapp.urls.delete")),  # delete
    path("", include("core.cooggerapp.urls.explorer")),  # explorer
    path("", include("core.cooggerapp.urls.home")),  # home
    path("", include("core.cooggerapp.urls.detail")),  # post detail
    path("", include("core.cooggerapp.urls.users")),  # users
    path("", include("core.cooggerapp.urls.sitemap")),  # sitemap
]
