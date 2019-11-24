from django.urls import path

from ..views.setting import (
    Address, DeleteAddress, Settings, UserExtra, UserSetMixin
)

urlpatterns = [
    path("", Settings.as_view(), name="settings"),
    path("address/", Address.as_view(), name="settings-address"),
    path("user/", UserSetMixin.as_view(), name="settings-user"),
    path("extra/", UserExtra.as_view(), name="settings-userextra"),
    path("delete/address/", DeleteAddress.as_view(), name="address_del"),
]
