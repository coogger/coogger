from django.conf.urls import url

#views
from apps.cooggerapp.views import csettings

urlpatterns = [
    url(r"^/profile/",csettings.ProfileBasedClass.as_view(),name = "sprofile"),
    url(r"^/account/",csettings.AccountBasedClass.as_view(),name = "saccount"),
    url(r"^/add-address/",csettings.AddaddessBasedClass.as_view(),name = "saddaddress"),
    url(r"^/",csettings.ProfileBasedClass.as_view(),name  ="settings"),
    ]
