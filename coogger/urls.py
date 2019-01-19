from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
# from django.urls import path

# common addresses
urlpatterns = [
    url(r"^accounts/", include('steemconnect_auth.urls')), # signup, login or create new user
    url(r'^admin/', admin.site.urls), # admin panel
    url(r"^api/",include("rest.urls")),
    url(r"^",include("cooggerapp.main_urls")), # home
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
