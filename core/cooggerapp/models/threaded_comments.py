# django
from django.db import models
from django.contrib.auth.models import User
from django.db.models import F
from django.utils.text import slugify
from django.utils import timezone

# python
import random


class ThreadedComments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permlink = models.SlugField(max_length=200)
    title = models.CharField(
        max_length=200, 
        help_text="Be sure to choose the best title", 
        null=True, 
        blank=True)
    reply = models.ForeignKey(
        "self", 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name="children")
    reply_count = models.IntegerField(default=0)
    # depth = models.IntegerField(default=0)
    created = models.DateTimeField(
        default=timezone.now, 
        verbose_name="Created")
    last_update = models.DateTimeField(
        default=timezone.now, 
        verbose_name="Last update")

    class Meta:
        ordering = ["-created"]
        abstract = True

    def __str__(self):
        return f"@{self.user}/{self.permlink}"

    def save(self, *args, **kwargs):
        if self.reply is not None:
            "if it is a comment"
            self.title = self.get_parent.title
            self.permlink = self.get_new_permlink(slugify(self.title.lower()))
            self.permlink = self.get_reply_permlink()
            self.set_reply_count(self.reply_id)
        else:
            self.permlink = self.get_new_permlink(slugify(self.title.lower()))
        super().save(*args, **kwargs)

    def set_reply_count(self, reply_id):
        while True:
            query = self.__class__.objects.filter(id=reply_id)
            if query.exists():
                query.update(
                        reply_count=(F("reply_count") + 1)
                    )
                if query[0].reply is not None:
                    reply_id = query[0].reply_id
                else:
                    break
            else:
                break

    def get_reply_permlink(self):
        return self.get_new_permlink(
            f"re-{str(self.user)}-re-{str(self.reply.user)}-{self.permlink}"
        )
    
    def get_new_permlink(self, permlink):
        while True:
            if self.__class__.objects.filter(
                user=self.user, 
                permlink=permlink).exists():
                permlink = permlink + "-" + str(random.randrange(9999999))
            else:
                break
        return permlink

    @property
    def get_parent(self):
        return self.__class__.objects.get(id=self.reply_id)

    @property
    def parent_username(self):
        return str(self.get_parent.user)

    @property
    def parent_permlink(self):
        return self.get_parent.permlink
