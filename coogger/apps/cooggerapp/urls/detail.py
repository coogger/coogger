from django.conf.urls import url

#views
from apps.cooggerapp.views import detail

urlpatterns = [
    url(r'^web/comment/$',detail.CommentClassBased.as_view(),name = "cooggerapp-comment"),
    url(r'^@(?P<username>.+)/(?P<utopic>.+)/(?P<path>.+)/$', detail.Detail.as_view(),name = "cooggerapp-detail"),
    ]
