from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
# from django.urls import path

# common addresses
urlpatterns = [
    url(r"^accounts/", include('core.steemconnect_auth.urls')), # signup, login or create new user
    url(r'^admin/', admin.site.urls), # admin panel
    url(r"^api/",include("core.api.urls")),
    url(r"^",include("core.cooggerapp.redirect_urls")), # home
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
