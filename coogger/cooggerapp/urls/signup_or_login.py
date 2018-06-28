from django.conf.urls import url
from django.http import HttpResponseRedirect

#views
from cooggerapp.views import signup_or_login

#modes
from cooggerapp.models import OtherInformationOfUsers

def redirect_home(request):
    otherinfo = OtherInformationOfUsers.objects.filter(user = request.user)
    if not otherinfo.exists():
        OtherInformationOfUsers(user = request.user).save()
        # steemconnect ile giriş yapıldıgı için
        # OtherInformationOfUsers kayıtlı olmuyor, değil ise kayıt ediyoruz.
    return HttpResponseRedirect("/web/feed/")

def login(request):
    return HttpResponseRedirect("/login/steemconnect/")

urlpatterns = [
    url(r"^/logout/",signup_or_login.Logout.as_view(),name = "cooggerapp-logout"),
    url(r"^/profile/",redirect_home),
    url(r"^/login/",login),
    ]
