#django
from django.http import HttpResponseRedirect
from django.contrib import messages as ms
from django.contrib.auth import logout,login
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
#models
from cooggerapp.models import OtherInformationOfUsers

from sc2py.client import Client
c = Client(client_id = "coogger.app",redirect_url = "http://127.0.0.1:8000/accounts/steemconnect/",code = True,scope = None)

def redirect_login(request):
    return HttpResponseRedirect(c.get_authorize_url())

def steemconnect(request):
    code = request.GET["code"]
    tokens = c.get_refresh_token(code = code,app_secret = "47499e12ba9e516bacd15686713ee36bfd8125e26e424a83")
    username = tokens["username"]
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    if User.objects.filter(username = username).exists():
        user = User.objects.filter(username = username)[0]
        OtherInformationOfUsers.objects.filter(user = user).update(
            code = code,
            access_token = access_token,
            refresh_token = refresh_token
            )
    else:
        import random
        user = User.objects.create_user(username = username, password = random.getrandbits(124)).save()
        user = User.objects.filter(username = username)[0]
        OtherInformationOfUsers(
            user = user,code = code,
            access_token = access_token,
            refresh_token = refresh_token
        ).save()
    login(request,user)
    # c.me(access_token = access_token)
    return HttpResponseRedirect("/web/feed/")

class Logout(View):
    error = "There was an unexpected error while exiting"
    success = "See you again {}"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            ms.success(request,self.success.format(request.user))
            logout(request)
        return HttpResponseRedirect("/")
