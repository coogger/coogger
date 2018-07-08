from django.conf.urls import url

#views
from cooggerapp.views import explorer

urlpatterns = [
    url(r'^tags/(?P<hashtag>.+)/',explorer.Hashtag.as_view(),name = "hashtag"),
    url(r'^list/(?P<list_>.+)/',explorer.Userlist.as_view(),name = "list"),
    url(r'^left_side/(?P<left>.+)/',explorer.LeftSide.as_view(),name = "left_side"),
    url(r'^right_side/(?P<right>.+)/',explorer.RightSide.as_view(),name = "right_side"),
    url(r'^filter',explorer.Filter.as_view(),name = "filter"),
    ]
