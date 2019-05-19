# django 
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# 3.part 
from django_md_editor.models import EditorMdField
from steemconnect_auth.models import SteemConnectUser

# choices
from core.cooggerapp.choices import FOLLOW, make_choices

# utils
from .utils import get_new_hash


class OtherInformationOfUsers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = EditorMdField()
    cooggerup_confirmation = models.BooleanField(
        default=False,
        verbose_name="Do you want to join in curation trails of the cooggerup bot with your account?",
    )
    sponsor = models.BooleanField(default=False)
    cooggerup_percent = models.FloatField(
        default=0, verbose_name="Cooggerup bot upvote percent"
    )
    vote_percent = models.FloatField(default=100)
    beneficiaries = models.IntegerField(
        default=0, verbose_name="Support Coogger ecosystem with beneficiaries"
    )
    # reward db of coogger.up curation trail, reset per week
    total_votes = models.IntegerField(default=0, verbose_name="How many votes")
    total_vote_value = models.FloatField(default=0, verbose_name="total vote value")
    access_token = models.CharField(max_length=500, default="no_permission")

    def save(self, *args, **kwargs):
        if self.access_token == "no_permission":
            self.access_token = self.get_new_access_token()
        super().save(*args, **kwargs)

    def get_new_access_token(self):
        """creates api_token and user save"""
        sc_user = SteemConnectUser.objects.filter(user=self.user)
        if sc_user.exists():
            return get_new_hash()
        return "no_permission"

    @property
    def username(self):
        return self.user.username

    @property
    def get_user(self):  # to api
        context = list()
        field = ("first_name", "last_name", "is_staff", "is_active", "id")
        for f in field:
            context.append({f: str(self.user.__getattribute__(f))})
        return context

    @property
    def get_steemconnect(self):
        context = list()
        field = ("access_token", "refresh_token", "code")
        for f in field:
            context.append({f: str(self.user.steemconnectuser.__getattribute__(f))})
        return context

    @property
    def get_user_address(self):  # to api
        context = list()
        queryset = self.user.otheraddressesofusers_set.filter(user=self.user)
        for u in queryset:
            context.append({"choice": u.choices, "address": u.address})
        return context


class OtherAddressesOfUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choices = models.CharField(
        blank=True,
        null=True,
        max_length=15,
        choices=make_choices(FOLLOW),
        verbose_name="website",
    )
    address = models.CharField(
        blank=True, null=True, max_length=50, verbose_name="write address / username"
    )

    @property
    def username(self):
        return self.user.username

    @property
    def get_addresses(self):
        try:
            return self.__class__.objects.filter(user=self.user)
        except:
            return []

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_otherinformationofusers(sender, instance, created, **kwargs):
    model = OtherInformationOfUsers
    if not model.objects.filter(user=instance).exists():
        model.objects.create(user=instance)