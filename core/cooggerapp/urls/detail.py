# django
from django.conf.urls import url

# views
from core.cooggerapp.views.detail import Embed, Detail


urlpatterns = [
    url(r'^embed/@(?P<username>.+)/(?P<permlink>.+)/$', Embed.as_view(), name="embed"),
    url(r'^@(?P<username>.+)/(?P<permlink>.+)/$', Detail.as_view(), name="detail"),
    ]
