# django
from django.urls import path
from django.shortcuts import redirect

# views
from core.cooggerapp.views.detail import Embed, Detail


def detail_redirect(request, category, username, permlink):
    return redirect(f"/@{username}/{permlink}")

urlpatterns = [
    path('embed/@<username>/<permlink>/', Embed.as_view(), name="embed"),
    path('<category>/@<username>/<permlink>/', detail_redirect, name="detail_redirect"),
    path('@<username>/<permlink>/', Detail.as_view(), name="detail"),
    ]
