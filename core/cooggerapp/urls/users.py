# django
from django.conf.urls import url

# views
from core.cooggerapp.views.users import About, Topic, Home, Comment, Wallet, Activity

urlpatterns = [
    # url(r'^upload/pp/$', users.Uploadpp.as_view(), name="user_upload_pp"),
    url(r"^about/@(?P<username>.+)/$", About.as_view(), name="userabout"),
    url(r'^(?P<topic>.+)/@(?P<username>.+)/$', Topic.as_view(), name="utopic"),
    url(r'^@(?P<username>.+)/$', Home.as_view(), name="user"),
    url(r'^comment/@(?P<username>.+)$', Comment.as_view(), name="comment"),
    url(r'^wallet/@(?P<username>.+)$', Wallet.as_view(), name="wallet"),
    url(r'^activity/@(?P<username>.+)$', Activity.as_view(), name="activity"),
    ]
