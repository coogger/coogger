from django.conf.urls import url

#views
from apps.cooggerapp.views import csettings

urlpatterns = [
    url(r"^/add-address/",csettings.Addaddess.as_view(),name = "cooggerapp-saddaddress"),
    url(r"^/cooggerapp-cooggerup/",csettings.Cooggerup.as_view(),name  ="cooggerapp-cooggerup"),
    url(r"^/cooggerapp-draft/",csettings.Draft.as_view(),name  ="cooggerapp-draft"),
    url(r"^/",csettings.Addaddess.as_view(),name  ="cooggerapp-settings"),
    ]
