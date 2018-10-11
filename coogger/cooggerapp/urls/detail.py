from django.conf.urls import url

# views
from cooggerapp.views import detail

urlpatterns = [
    url(r'^embed/@(?P<username>.+)/(?P<path>.+)/$', detail.Embed.as_view(), name="embed"),
    url(r'^@(?P<username>.+)/(?P<path>.+)/$', detail.Detail.as_view(), name="detail"),
    ]
