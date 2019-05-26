# django 
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.db.utils import IntegrityError

# 3.part 
from django_md_editor.models import EditorMdField

# choices
from core.cooggerapp.choices import FOLLOW, make_choices

# utils
from .utils import get_new_hash


class OtherInformationOfUsers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = EditorMdField(blank=True, null=True)
    access_token = models.CharField(max_length=500, default=get_new_hash)

    @property
    def username(self):
        return str(self.user)

    @property
    def get_user(self):  # to api
        context = list()
        field = ("first_name", "last_name", "is_staff", "is_active", "id")
        for f in field:
            context.append({f: str(self.user.__getattribute__(f))})
        return context

    @property
    def get_user_address(self):  # to api
        context = list()
        queryset = self.user.otheraddressesofusers_set.filter(user=self.user)
        for u in queryset:
            context.append({"choice": u.choices, "address": u.address})
        return context


class OtherAddressesOfUsers(models.Model):
    "maybe ManyToManyField in OtherInformationOfUsers"
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
    # TODO get follow and following list and save OtherInformationOfUsers 
    if created:
        OtherInformationOfUsers(user=instance).save()
        # o = OtherInformationOfUsers.objects.get(user_id=1)
        # o.follower.add(instance)