# django
from django.urls import path
from django.shortcuts import redirect

# views
from core.cooggerapp.views.detail import Embed, Detail, Commits, CommitDetail


def detail_redirect(request, category, username, permlink):
    return redirect(f"/@{username}/{permlink}")


urlpatterns = [
    path('@<username>/<topic>/commit/<hash>/', CommitDetail.as_view(), name="commit"),
    path('@<username>/<topic>/commits/', Commits.as_view(), name="commits"),
    path('embed/@<username>/<permlink>/', Embed.as_view(), name="embed"),
    path('<category>/@<username>/<permlink>/', detail_redirect, name="detail_redirect"),
    path('@<username>/<permlink>/', Detail.as_view(), name="detail"),
    ]
