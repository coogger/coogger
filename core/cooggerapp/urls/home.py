# django
from django.urls import path

# views
from core.cooggerapp.views.home import Home, Search, Report, Review

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('search/', Search.as_view(), name="search"),
    path('report/', Report.as_view(), name="report"),
    path('review/', Review.as_view(), name="review"),
    ]
