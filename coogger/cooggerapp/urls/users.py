# django
from django.conf.urls import url

# views
from cooggerapp.views import users

urlpatterns = [
    # url(r'^upload/pp/$', users.Uploadpp.as_view(), name="user_upload_pp"),
    url(r"^web/following/$", users.FollowBaseClass.as_view(), name="following"),
    url(r"^web/about/@(?P<username>.+)/$", users.UserAboutBaseClass.as_view(), name="userabout"),
    url(r'^(?P<utopic>.+)/@(?P<username>.+)/$', users.UserTopic.as_view(), name="utopic"),
    url(r'^@(?P<username>.+)/$', users.UserClassBased.as_view(), name="user"),
    ]
