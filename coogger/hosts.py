from django.conf import settings
from django_hosts import patterns, host
from django.conf.urls import include, url

api_urlpatterns = [
    url(r"^api/",include("cooggerapi.urls")),
]



host_patterns = patterns('',
    host(r'www', settings.ROOT_URLCONF, name='www'),
    host(r'api', api_urlpatterns, name='api'),
)
