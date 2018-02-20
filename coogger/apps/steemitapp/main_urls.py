# django
from django.conf.urls import include, url

urlpatterns = [
    url(r"",include("apps.steemitapp.urls.home")),
    url(r"^convert",include("apps.steemitapp.urls.convert")),
]
