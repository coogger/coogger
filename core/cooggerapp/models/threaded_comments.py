# django
from django.db import models
from django.contrib.auth.models import User
from django.db.models import F
from django.utils.text import slugify

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
        auto_now_add=True, 
        verbose_name="Created")
    last_update = models.DateTimeField(
        auto_now_add=True, 
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
            self.permlink = self.get_new_permlink(self.get_reply_permlink())
            for obj in self.get_all_reply_obj():
                obj.update(
                        reply_count=(F("reply_count") + 1)
                    )
        else:
            self.permlink = self.get_new_permlink(slugify(self.title.lower()))
        super().save(*args, **kwargs)

    def get_all_reply_obj(self):
        reply_id = self.reply_id
        while True:
            query = self.__class__.objects.filter(id=reply_id)
            if query.exists():
                yield query
                if query[0].reply is not None:
                    reply_id = query[0].reply_id
                else:
                    break
            else:
                break

    def get_reply_permlink(self):
        return self.get_new_permlink(
            f"re-{str(self.user)}-re-{str(self.reply.user)}-{slugify(self.title.lower())}"
        )
    
    def get_new_permlink(self, permlink):
        while True:
            if self.__class__.objects.filter(user=self.user, permlink=permlink).exists():
                permlink = permlink + "-" + str(random.randrange(9999999))
            else:
                break
        return permlink

    @property
    def get_parent(self):
        if self.reply is None:
            return self
        return self.__class__.objects.get(id=self.reply_id)

    @property
    def parent_user(self):
        return self.get_parent.user

    @property
    def parent_permlink(self):
        return self.get_parent.permlink
