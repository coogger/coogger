from django.conf.urls import url

#views
from cooggerapp.views import explorer

urlpatterns = [
    url(r'^/tags/(?P<hashtag>.+)/',explorer.Hashtag.as_view(),name = "cooggerapp-hashtag"),
    url(r'^/list/(?P<list_>.+)/',explorer.Userlist.as_view(),name = "cooggerapp-list"),
    ]
