from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", User)


class Badges(models.Model):
    title = models.CharField(unique=True, max_length=120)
    permlink = models.CharField(max_length=120)
    image_address = models.URLField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        self.permlink = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class UserBadge(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    badge = models.ManyToManyField(Badges)

    def __str__(self):
        return str(self.user)

    def get_badges(self):
        return self.badge.all()

    def get_badge_count(self):
        return self.badge.count()
