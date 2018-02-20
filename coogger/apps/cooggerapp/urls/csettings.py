from django.conf.urls import url

#views
from apps.cooggerapp.views import csettings

urlpatterns = [
    url(r"^/profile/",csettings.Profile.as_view(),name = "cooggerapp-sprofile"),
    url(r"^/account/",csettings.Account.as_view(),name = "cooggerapp-saccount"),
    url(r"^/add-address/",csettings.Addaddess.as_view(),name = "cooggerapp-saddaddress"),
    url(r"^/",csettings.Profile.as_view(),name  ="cooggerapp-settings"),
    ]
