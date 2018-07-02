from django.conf.urls import url
from django.http import HttpResponseRedirect

#views
from cooggerapp.views import signup_or_login

#modes
from cooggerapp.models import OtherInformationOfUsers



urlpatterns = [
    url(r"^/logout/",signup_or_login.Logout.as_view(),name = "logout"),
    url(r"^/login/",signup_or_login.redirect_login,name = "login"),
    url(r"^/steemconnect/",signup_or_login.steemconnect,name = "steemconnect"),
    ]
