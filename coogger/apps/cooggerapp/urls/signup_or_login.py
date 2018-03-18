from django.conf.urls import url
from django.http import HttpResponseRedirect

#views
from apps.cooggerapp.views import signup_or_login
import views as app_views

def redirect(request):
    return HttpResponseRedirect("https://signup.steemit.com/")

urlpatterns = [
    url(r"^/signup/",redirect,name = "cooggerapp-signup"),
    url(r"^/login/",app_views.home,name = "cooggerapp-login"),
    url(r"^/logout/",signup_or_login.Logout.as_view(),name = "cooggerapp-logout"),
    ]
