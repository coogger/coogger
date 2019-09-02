from django.contrib.auth.models import User
from django.db import models
from django_md_editor.models import EditorMdField

from core.cooggerapp.choices import FOLLOW, TITLES, make_choices


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
    about = EditorMdField(
        help_text="Write a long article about yourself, see; /u/@your_username/about/",
        verbose_name="About Yourself",
        blank=True,
        null=True,
    )
    bio = models.CharField(
        help_text="Write something short about yourself, this will appear in your profile.",
        max_length=260,
        blank=True,
        null=True,
    )
    address = models.ManyToManyField(OtherAddressesOfUsers, blank=True)
    email_permission = models.BooleanField(
        help_text="Allow email notifications.", default=True
    )
    title = models.CharField(
        max_length=30,
        default="user",
        choices=make_choices(TITLES),
        verbose_name="title",
        help_text="Title",
    )
    # company = TODO
    def __str__(self):
        return str(self.user)
