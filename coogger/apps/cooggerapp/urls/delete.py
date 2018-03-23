from django.conf.urls import url

#views
from apps.cooggerapp.views import delete

urlpatterns = [
    url(r'^/address/',delete.Address.as_view(),name="cooggerapp-address_del"),
    ]
