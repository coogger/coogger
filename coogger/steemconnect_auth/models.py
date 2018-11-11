from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django_md_editor.models import EditorMdField

class Dapp(models.Model):
    name = models.CharField(max_length=20, unique=True)
    host_name = models.CharField(max_length=30, unique=True)
    redirect_url = models.CharField(max_length=400, unique=True)
    client_id = models.CharField(max_length=200)
    app_secret = models.CharField(max_length=400)
    login_redirect = models.CharField(max_length=50)
    default_scope = "login, offline, vote, comment, comment_options, delete_comment, custom_json, claim_reward_balance"
    scope = models.CharField(default=default_scope, max_length=200)
    icon_address = models.CharField(max_length=400)
    ms = models.CharField(max_length=1000)
    management = models.ForeignKey(User, on_delete=models.CASCADE)
    definition = models.CharField(max_length=900)
    image = models.CharField(max_length=400)
    active = models.BooleanField(default=True)
    beneficiaries = models.IntegerField(default=0)

    @property
    def management_user(self):
        return self.management.username

    def __str__(self):
        return self.name


class Mods(models.Model):
    dapp = models.ForeignKey(Dapp, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def dapp_name(self):
        return self.dapp.name

    @property
    def username(self):
        return self.user.username

    def __str__(self):
        return self.dapp.name


class SteemConnectUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dapp = models.ForeignKey(Dapp, on_delete=models.CASCADE, help_text="dapp", default=1)
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

    @property
    def dapp_name(self):
        return self.dapp.name

    def __str__(self):
        return self.user.username


class DappSettings(models.Model):
    dapp = models.ForeignKey(Dapp, on_delete=models.CASCADE)
    beneficiaries = models.FloatField(default=0,
        verbose_name="Support Coogger ecosystem with beneficiaries"
    )


class CategoryofDapp(models.Model):
    dapp = models.ForeignKey(Dapp, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50, verbose_name="Category name")
    editor_template = EditorMdField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.category_name = slugify(self.category_name)
        super(CategoryofDapp, self).save(*args, **kwargs)
