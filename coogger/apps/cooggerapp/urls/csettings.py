from django.conf.urls import url

#views
from apps.cooggerapp.views import csettings

urlpatterns = [
    url(r"^/add-address/",csettings.Addaddess.as_view(),name = "cooggerapp-saddaddress"),
    url(r"^/votepercent/",csettings.Vote.as_view(),name = "cooggerapp-votepercent"),
    url(r"^/cooggerup/",csettings.Cooggerup.as_view(),name  ="cooggerapp-cooggerup"),
    url(r"^/draft/",csettings.Draft.as_view(),name  ="cooggerapp-draft"),
    url(r"^/",csettings.Addaddess.as_view(),name  ="cooggerapp-settings"),
    ]
