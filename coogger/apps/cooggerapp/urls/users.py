# django
from django.conf.urls import url

#views
from apps.cooggerapp.views import users

urlpatterns = [
    # url(r'^upload/pp/$',users.Uploadpp.as_view(),name="cooggerapp-user_upload_pp"),
    url(r"^web/following/$",users.FollowBaseClass.as_view(),name="cooggerapp-following"),
    url(r"^web/about/@(?P<username>.+)/$",users.UserAboutBaseClass.as_view(),name="cooggerapp-userabout"),
    url(r'^@(?P<username>.+)/(?P<utopic>.+)/$', users.UserTopic.as_view(),name = "cooggerapp-utopic"),
    url(r'^@(?P<username>.+)/$', users.UserClassBased.as_view(),name = "cooggerapp-user"),
    ]
