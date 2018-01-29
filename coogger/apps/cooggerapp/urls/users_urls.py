from django.conf.urls import url

#views
from apps.cooggerapp.views import users

urlpatterns = [
    url(r'^upload/pp/$',users.UploadppBasedClass.as_view(),name="user_upload_pp"),
    url(r"^web/following/$",users.FollowBaseClass.as_view(),name="following"),
    url(r"^web/about/(?P<username>.+)/$",users.UserAboutBaseClass.as_view(),name="userabout"),
    url(r'^(?P<username>.+)/(?P<utopic>.+)/$', users.UserTopicBasedClass.as_view(),name = "utopic"),
    url(r'^(?P<username>.+)/$', users.UserBasedClass.as_view(),name = "user"),
    ]
