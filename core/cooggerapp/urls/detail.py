# django
from django.conf.urls import url
from django.shortcuts import redirect

# views
from core.cooggerapp.views.detail import Embed, Detail, Commits, CommitDetail


def detail_redirect(request, category, username, permlink):
    return redirect(f"/@{username}/{permlink}")


urlpatterns = [
    url(r'^@(?P<username>.+)/(?P<topic>.+)/commit/(?P<hash>.+)/$', CommitDetail.as_view(), name="commit"),
    url(r'^@(?P<username>.+)/(?P<topic>.+)/commits/$', Commits.as_view(), name="commits"),
    url(r'^embed/@(?P<username>.+)/(?P<permlink>.+)/$', Embed.as_view(), name="embed"),
    url(r'^(?P<category>.+)/@(?P<username>.+)/(?P<permlink>.+)/$', detail_redirect, name="detail_redirect"),
    url(r'^@(?P<username>.+)/(?P<permlink>.+)/$', Detail.as_view(), name="detail"),
    ]
