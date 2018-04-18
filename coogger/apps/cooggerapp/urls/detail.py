from django.conf.urls import url

#views
from apps.cooggerapp.views import detail

urlpatterns = [
    url(r'^@(?P<username>.+)/(?P<content_list>.+)/(?P<path>.+)/$', detail.Detail.as_view(),name = "cooggerapp-detail"),
    ]
