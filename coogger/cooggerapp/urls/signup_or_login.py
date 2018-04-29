from django.conf.urls import url
from django.http import HttpResponseRedirect

#views
from cooggerapp.views import signup_or_login

#modes
from cooggerapp.models import OtherInformationOfUsers

def redirect(request):
    return HttpResponseRedirect("https://signup.steemit.com/")

def redirect_home(request):
    otherinfo = OtherInformationOfUsers.objects.filter(user = request.user)
    if not otherinfo.exists():
        OtherInformationOfUsers(user = request.user).save()
        # steemconnect ile giriş yapıldıgı için
        # OtherInformationOfUsers kayıtlı olmuyor, değil ise kayıt ediyoruz.
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
