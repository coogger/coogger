from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r"^",include("apps.cooggerapp.urls.home_urls")), # home
    url(r"^",include("apps.cooggerapp.urls.seo_urls")), # seo
    url(r"^post",include("apps.cooggerapp.urls.controls_urls")), # post
    url(r"^settings",include("apps.cooggerapp.urls.csettings_urls")), # settings
    url(r"^delete",include("apps.cooggerapp.urls.delete_urls")), # delete
    url(r"^explorer",include("apps.cooggerapp.urls.explorer_urls")), # explorer
    url(r"^accounts",include("apps.cooggerapp.urls.signup_or_login_urls")), # accounts işlemleri
    url(r'^web/admin/', admin.site.urls), # admin panel
    url(r'^web/ckeditor/', include('ckeditor_uploader.urls')), # ckeditör
    url(r"^",include("apps.cooggerapp.urls.detail_urls")), # post detail
    url(r"^",include("apps.cooggerapp.urls.users_urls")), # users en sonda olması gerek
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
