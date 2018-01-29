from django.conf.urls import url

#views
from apps.cooggerapp.views import detail

urlpatterns = [
    url(r'^web/comment/$',detail.CommentBasedClass.as_view(),name = "comment"),
    url(r'^(?P<username>.+)/(?P<utopic>.+)/(?P<path>.+)/$', detail.DetailBasedClass.as_view(),name = "detail"),
    ]
