from django.conf.urls import url

# views
from cooggerapp.views import post

urlpatterns = [
    url(r'^create/$', post.Create.as_view(), name="create"),
    url(r'^change/@(?P<username>.+)/(?P<permlink>.+)/$', post.Change.as_view(), name="change"),
    ]
