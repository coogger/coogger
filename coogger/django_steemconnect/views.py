#django
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages as ms
from django.contrib.auth import logout,login
from django.views import View
from django.contrib.auth.models import User
from django.conf import settings

# models
from django_steemconnect.models import SteemConnectUser
from cooggerapp.views.tools import get_community_model

# python steemconnect-client
from sc2py.client import Client

import random

class LoginSignup(View):

    def get(self, request, *args, **kwargs):
        code = request.GET["code"]
        community_model = get_community_model(request)
        tokens = get_client(request).get_refresh_token(code,community_model.app_secret)
        username = tokens["username"]
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]
        user, created = User.objects.get_or_create(username = username)
        if created: # TODO:  burayı daha moduler kullanısşı hale getir.
            from cooggerapp.models import OtherInformationOfUsers
            OtherInformationOfUsers(user = user).save()
        if SteemConnectUser.objects.filter(user = user).exists():
            SteemConnectUser.objects.filter(user = user).update(
                code = code,
                access_token = access_token,
                refresh_token = refresh_token,
                community_name = community_model.name,
                )
        else:
            SteemConnectUser(
                user = user,code = code,
                access_token = access_token,
                refresh_token = refresh_token,
                community_name = community_model.name,
                ).save()
        login(request,user)
        return HttpResponseRedirect(community_model.login_redirect)


def get_client(request):
    community_model = get_community_model(request)
    return Client(client_id = community_model.client_id,
        redirect_url = community_model.redirect_url,
        code = True,
        scope = community_model.scope
    )


def login_redirect(request):
    return HttpResponseRedirect(get_client(request).get_authorize_url())

class Logout(View):
    error = "There was an unexpected error while exiting"
    success = "See you again {}"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            ms.success(request,self.success.format(request.user))
            logout(request)
        return HttpResponseRedirect("/")
