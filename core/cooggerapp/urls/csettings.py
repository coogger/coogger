from django.conf.urls import url

# views
from core.cooggerapp.views import csettings

urlpatterns = [
    url(r"^/", csettings.Settings.as_view(), name="settings"),
    ]
