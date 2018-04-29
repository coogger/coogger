from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from django.urls import path

#views
from views import AppsHome
# from views import AppsSitemap
from django.contrib.sitemaps.views import sitemap

# common addresses
urlpatterns = [
    url(r'^web/admin/', admin.site.urls), # admin panel
    url(r"^apps/cooggerup/",include("cooggerup.urls")),
]

# main project = coogger
urlpatterns += [
    url(r"^",include("cooggerapp.main_urls")), # home
    url(r'', include('social_django.urls'))
]

# apps mainpage
urlpatterns += [
    url(r'^apps/$',AppsHome.as_view(),name="apps-home"),
    # url(r'^sitemap/apps\.xml/$', sitemap, {'sitemaps': {"apps":AppsSitemap()}}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
