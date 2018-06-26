from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.sitemaps.views import sitemap

# common addresses
urlpatterns = [
    url(r"^",include("cooggerapp.main_urls")), # home
    url(r'', include('social_django.urls')),
    url(r'^web/admin/', admin.site.urls), # admin panel
    url(r"^api/",include("api.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
