from django.conf.urls import url

#views
from apps.cooggerapp.views import explorer

urlpatterns = [
    url(r'^/tags/(?P<hashtag>.+)/',explorer.HashtagBasedClass.as_view(),name = "hashtag"),
    url(r'^/list/(?P<list_>.+)/',explorer.UserlistBasedClass.as_view(),name = "list"),
    ]
