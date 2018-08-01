from django.db import models
from django.contrib.auth.models import User


class Community(models.Model):
    name = models.CharField(max_length=20, unique=True)
    host_name = models.CharField(max_length=30, unique=True)
    redirect_url = models.CharField(max_length=400, unique=True)
    client_id = models.CharField(max_length=200, unique=True)
    app_secret = models.CharField(max_length=400, unique=True)
    login_redirect = models.CharField(max_length=50)
    default_scope = "vote,comment_options,comment,offline"
    scope = models.CharField(default=default_scope, max_length=200)
    icon_address = models.CharField(max_length=400)
    ms = models.CharField(max_length=500)
    management = models.ForeignKey(User, on_delete=models.CASCADE)  # admin for community


class Mods(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def community_name(self):
        return self.community.name

    @property
    def username(self):
        return self.user.username


class SteemConnectUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, help_text="community", default=1)
    refresh_token = models.CharField(max_length=500, help_text="steemconnect user code / to get get_refresh_token")
    code = models.CharField(max_length=500, help_text="steemconnect user code / to get get_refresh_token")
    access_token = models.CharField(max_length=500, help_text="steemconnect user access_token to any operations")

    def set_new_access_token(self, secret):
        tokens = Client.get_refresh_token(code=self.code, app_secret=secret)
        access_token = tokens["access_token"]
        SteemConnectUser.objects.filter(user=self.user).update(access_token=access_token)
        return access_token

    @property
    def username(self):
        return self.user.username
