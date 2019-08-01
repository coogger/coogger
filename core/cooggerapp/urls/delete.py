from django.urls import path

from ..views import delete

urlpatterns = [path("address/", delete.Address.as_view(), name="address_del")]
