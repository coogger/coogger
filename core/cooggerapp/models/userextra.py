# django 
from django.contrib.auth.models import User
from django.db import models

# django lib
from django_md_editor.models import EditorMdField

# choices
from core.cooggerapp.choices import FOLLOW, make_choices


class OtherAddressesOfUsers(models.Model):
    "maybe ManyToManyField in UserProfile"
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

    def __str__(self):
        return f"{self.choices} - {self.address}"

    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = EditorMdField(blank=True, null=True)
    address = models.ManyToManyField(
        OtherAddressesOfUsers,
        blank=True,
    )
    email_permission = models.BooleanField(default=True)