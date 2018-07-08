from django.conf.urls import url
from django.http import HttpResponseRedirect
from django.views.generic.base import RedirectView

#views
from django_steemconnect.views import Logout,LoginSignup,login_redirect

urlpatterns = [
    url(r"^logout/",Logout.as_view(),name = "logout"),
    url(r"^login/",login_redirect,name = "login"),
    url(r"^steemconnect/",LoginSignup.as_view(),name = "steemconnect"),
    ]
