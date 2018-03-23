from django.conf.urls import url
from django.http import HttpResponseRedirect

#views
from apps.cooggerapp.views import signup_or_login

def redirect(request):
    return HttpResponseRedirect("https://signup.steemit.com/")

def redirect_home(request):
    return HttpResponseRedirect("/@"+request.user.username)

from decorators import render_to
@render_to('login.html')
def login(request):
    pass

urlpatterns = [
    url(r"^/signup/",redirect,name = "cooggerapp-signup"),
    url(r"^/login/",login,name = "cooggerapp-login"),
    url(r"^/logout/",signup_or_login.Logout.as_view(),name = "cooggerapp-logout"),
    url(r"^/profile/",redirect_home),
    ]
