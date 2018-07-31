from django.conf.urls import url

# views
from cooggerapp.views import detail

urlpatterns = [
    url(r'^@(?P<username>.+)/(?P<path>.+)/$', detail.Detail.as_view(), name="detail"),
    ]
