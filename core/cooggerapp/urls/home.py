# django
from django.urls import path

# views
from ..views.home import Home, Search, Report

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('search/', Search.as_view(), name="search"),
    path('report/<content_id>/', Report.as_view(), name="report"),
    
    ]
