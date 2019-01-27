# django
from django.conf.urls import url
from django.shortcuts import redirect
from django.contrib.auth import authenticate

# views
from core.cooggerapp.views import detail

# model
from core.cooggerapp.models import Content


def redirect_detail(request, username, permlink):
    user = authenticate(username=username)
    topic = Content.objects.filter(user=user, permlink=permlink)[0].topic
    return redirect(f"/{topic}/@{username}/{permlink}")

urlpatterns = [
    url(r'^embed/@(?P<username>.+)/(?P<path>.+)/$', detail.Embed.as_view(), name="embed"),
    url(r'^(?P<topic>.+)/@(?P<username>.+)/(?P<permlink>.+)/$', detail.Detail.as_view(), name="detail"),
    url(r'^@(?P<username>.+)/(?P<permlink>.+)/$', redirect_detail, name="redirect_detail"),
    ]
