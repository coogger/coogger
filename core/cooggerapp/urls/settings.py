from django.urls import path

from ..views.settings import Address, Settings, User, UserExtra

urlpatterns = [
    path("", Settings.as_view(), name="settings"),
    path("address/", Address.as_view(), name="settings-address"),
    path("user/", User.as_view(), name="settings-user"),
    path("user-extra/", UserExtra.as_view(), name="settings-userextra"),
]
