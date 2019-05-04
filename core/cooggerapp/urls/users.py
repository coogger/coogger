# django
from django.urls import path

# views
from core.cooggerapp.views.users import (About, Home, Comment, Wallet, Activity)

urlpatterns = [
    # url(r'^upload/pp/$', users.Uploadpp.as_view(), name="user_upload_pp"),
    path('about/@<username>/', About.as_view(), name="userabout"),
    path('@<username>/', Home.as_view(), name="user"),
    path('comment/@<username>', Comment.as_view(), name="comment"),
    path('wallet/@<username>', Wallet.as_view(), name="wallet"),
    path('activity/@<username>', Activity.as_view(), name="activity"),
    ]
