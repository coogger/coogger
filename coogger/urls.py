from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from core.cooggerapp.models import get_new_hash


# common addresses
urlpatterns = [
    path("accounts/", include('steemconnect_auth.urls')), # signup, login or create new user
    path(f"{get_new_hash()}/", admin.site.urls), # admin panel
    path("api/", include("core.api.urls")),
    path("", include("core.cooggerapp.redirect_urls")), # home
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
