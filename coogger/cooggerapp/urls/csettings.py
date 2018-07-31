from django.conf.urls import url

# views
from cooggerapp.views import csettings

urlpatterns = [
    url(r"^/", csettings.Settings.as_view(), name="settings"),
    ]
