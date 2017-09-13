from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]

"""
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r"",include("cosapp.urls")),
    url(r"^radio",include("radio.urls")),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
"""
