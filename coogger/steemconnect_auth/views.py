# django
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages as ms
from django.contrib.auth import logout, login
from django.views import View
from django.contrib.auth.models import User
from django.conf import settings

# models
from steemconnect_auth.models import SteemConnectUser, Dapp
from cooggerapp.models import OtherInformationOfUsers

# python steemconnect
from steemconnect.client import Client

import random


def get_client(request):
    dapp_model = request.dapp_model
    return Client(
        client_id=dapp_model.client_id,
        redirect_url=dapp_model.redirect_url,
        code=True,
        scope=dapp_model.scope
    )


def login_redirect(request):
    return HttpResponseRedirect(get_client(request).get_authorize_url())


class LoginSignup(View):

    def get(self, request, *args, **kwargs):
        code = request.GET["code"]
        dapp_model = request.dapp_model
        client = get_client(request)
        tokens = client.get_refresh_token(code, dapp_model.app_secret)
        username = tokens["username"]
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]
        user, created = User.objects.get_or_create(username=username)
        if created:
            OtherInformationOfUsers(
                user=user,
                access_token=access_token
            ).save_with_access_token() # create a new access_token for using coogger api with using steem access_token
        if SteemConnectUser.objects.filter(user=user).exists():
            SteemConnectUser.objects.filter(user=user).update(
                code=code,
                access_token=access_token,
                refresh_token=refresh_token,
                dapp=dapp_model,
                )
        else:
            SteemConnectUser(
                user=user, code=code,
                access_token=access_token,
                refresh_token=refresh_token,
                dapp=dapp_model,
                ).save()
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return HttpResponseRedirect(dapp_model.login_redirect)


class Logout(View):
    error = "There was an unexpected error while exiting"
    success = "See you again {}"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            ms.success(request, self.success.format(request.user))
            logout(request)
        return HttpResponseRedirect("/")
