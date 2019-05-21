# django
from django.urls import path
from django.shortcuts import redirect

# views
from core.cooggerapp.views.detail import Embed, Detail


urlpatterns = [
    path('embed/@<username>/<permlink>/', Embed.as_view(), name="embed"),
    path('@<username>/<permlink>/', Detail.as_view(), name="detail"),
    ]
