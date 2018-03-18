from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

#views
from apps.views import AppsHome
from apps.views import AppsSitemap
from django.contrib.sitemaps.views import sitemap

# common addresses
urlpatterns = [
    url(r'^web/admin/', admin.site.urls), # admin panel
    url(r'^web/ckeditor/', include('ckeditor_uploader.urls')), # ckeditör
]


import views as app_views

urlpatterns = [
    url(r'^logout/$', app_views.logout),
    url(r'^done/$', app_views.done, name='done'),
    url(r'', include('social_django.urls'))
]

# main project = coogger
urlpatterns += [
    url(r"^",include("apps.cooggerapp.main_urls")), # home
]

# apps mainpage
urlpatterns += [
    url(r'^apps/$',AppsHome.as_view(),name="apps-home"),
    url(r'^sitemap/apps\.xml/$', sitemap, {'sitemaps': {"apps":AppsSitemap()}}),
]

# other apps - her uygulama main_urls.py adında bir dosya açmalı ve adreslerini oraya koymalı - ordan başka yere yönlendirebilir.
for apps in settings.INSTALLED_APPS:
    if apps.startswith("apps."):
        app_name = apps.split(".")[1]
        if app_name != "cooggerapp":
            urlpatterns += [
                url(r"^apps/{}/".format(app_name),include("apps.{}.main_urls".format(app_name))),
            ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
