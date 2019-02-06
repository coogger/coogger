from django.conf.urls import url

# views
from core.cooggerapp.views.post import Create, Change, CreateUTopic, UpdateUTopic

urlpatterns = [
    url(r'^utopic/(?P<name>.+)/$', UpdateUTopic.as_view(), name="update-utopic"),
    url(r'^utopic/$', CreateUTopic.as_view(), name="create-utopic"),
    url(r'^create/$', Create.as_view(), name="create"),
    url(r'^change/@(?P<username>.+)/(?P<permlink>.+)/$', Change.as_view(), name="change"),
    ]
