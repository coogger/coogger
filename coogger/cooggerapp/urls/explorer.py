from django.conf.urls import url

#views
from cooggerapp.views import explorer

urlpatterns = [
    url(r'^tags/(?P<hashtag>.+)/',explorer.Hashtag.as_view(),name = "cooggerapp-hashtag"),
    url(r'^list/(?P<list_>.+)/',explorer.Userlist.as_view(),name = "cooggerapp-list"),
    url(r'^language/(?P<lang>.+)/',explorer.Language.as_view(),name = "cooggerapp-language"),
    url(r'^category/(?P<cat>.+)/',explorer.Category.as_view(),name = "cooggerapp-category"),
    ]
