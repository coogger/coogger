from django.conf.urls import url

#views
from apps.cooggerapp.views import home

urlpatterns = [
    url(r'^$', home.HomeBasedClass.as_view(),name = "home"),
    url(r'^web/search/$',home.SearchBasedClass.as_view(),name = "search"),
    url(r'^web/report/$',home.ReportBasedClass.as_view(),name = "report"),
    url(r'^web/notification/$',home.NotificationBasedClass.as_view(),name = "notification"),
    url(r"^web/following/content/$",home.FollowingContentBasedClass.as_view(),name="followingcontent"),
    ]
